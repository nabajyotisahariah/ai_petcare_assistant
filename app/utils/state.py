import json
import redis
from typing import Optional, Dict, Any
from app.config import settings

class ConversationState:
    def __init__(self):
        # Fallback to in-memory dictionary if Redis connection fails for MVP purposes
        self._memory_store = {}
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            self.redis_client.ping()
            self.use_redis = True
        except (redis.ConnectionError, redis.TimeoutError):
            self.use_redis = False
            print("WARNING: Could not connect to Redis. Falling back to in-memory state store for MVP.")

    def get_state(self, session_id: str) -> Dict[str, Any]:
        if self.use_redis:
            data = self.redis_client.get(f"session:{session_id}")
            return json.loads(data) if data else {}
        else:
            return self._memory_store.get(session_id, {})

    def update_state(self, session_id: str, updates: Dict[str, Any]):
        state = self.get_state(session_id)
        state.update(updates)
        if self.use_redis:
            self.redis_client.set(f"session:{session_id}", json.dumps(state), ex=3600) # 1 hour expiry
        else:
            self._memory_store[session_id] = state

    def set_pending_action(self, session_id: str, action: str, params: Dict[str, Any]):
        self.update_state(session_id, {
            "pending_action": action,
            "action_parameters": params,
            "requires_confirmation": True
        })

    def clear_pending_action(self, session_id: str):
        state = self.get_state(session_id)
        state.pop("pending_action", None)
        state.pop("action_parameters", None)
        state["requires_confirmation"] = False
        if self.use_redis:
            self.redis_client.set(f"session:{session_id}", json.dumps(state), ex=3600)
        else:
            self._memory_store[session_id] = state

state_manager = ConversationState()
