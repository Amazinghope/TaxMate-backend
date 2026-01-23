## POST /session/start
Request:
{
  "persona": "freelancer",
  "state": "Lagos",
  "mode": "pidgin"
}

Response:
{
  "session_id": "abc123"
}

## POST /session/update
Request:
{
  "session_id": "abc123",
  "persona": "business_owner",
  "mode": "eli5"
}


## POST /chat
Request:
{
  "session_id": "abc123",
  "message": "Which taxes apply to me?"
}

Response:
{
  "reply": "..."
}
