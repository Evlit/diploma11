from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    username: str | None


class Message(BaseModel):
    chat: Chat
    text: str | None = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdateResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
