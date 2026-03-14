import asyncio
import uuid
import logging

class SwarmMessage:
    def __init__(self, sender_id, receiver_id, action, payload):
        self.message_id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.action = action
        self.payload = payload

class NodeManager:
    """The 'Brain' router that manages nodes and inference."""
    def __init__(self):
        self.nodes = {}
        self.message_queue = asyncio.Queue()
        self.running = False

    def register_node(self, node_id, node):
        self.nodes[node_id] = node
        logging.info(f"Node {node_id} registered.")

    async def start(self):
        self.running = True
        asyncio.create_task(self._process_messages())

    async def stop(self):
        self.running = False

    async def _process_messages(self):
        while self.running:
            try:
                msg = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                if msg.receiver_id in self.nodes:
                    await self.nodes[msg.receiver_id].receive(msg)
                elif msg.receiver_id == "brain":
                    await self._handle_brain_logic(msg)
                else:
                    logging.warning(f"Unknown receiver: {msg.receiver_id}")
            except asyncio.TimeoutError:
                continue

    async def send(self, msg: SwarmMessage):
        await self.message_queue.put(msg)
        
    async def _handle_brain_logic(self, msg: SwarmMessage):
        # Decoupled Inference Logic
        response_payload = {"status": "processed", "result": f"Inference for {msg.action}"}
        response = SwarmMessage("brain", msg.sender_id, "response", response_payload)
        await self.send(response)


class AgentActor:
    """The 'Body' that executes logic but defers inference to NodeManager via RPC."""
    def __init__(self, actor_id, node_manager: NodeManager):
        self.actor_id = actor_id
        self.node_manager = node_manager
        self.node_manager.register_node(self.actor_id, self)

    async def send_to_brain(self, action, payload):
        msg = SwarmMessage(self.actor_id, "brain", action, payload)
        await self.node_manager.send(msg)

    async def receive(self, msg: SwarmMessage):
        logging.info(f"[{self.actor_id}] Received: {msg.action} - {msg.payload}")
