# Frontend API Contract

Frontend should interact ONLY with these endpoints.

---

## Search

**GET** `/api/search?q=<query>`

Example:
```
http://127.0.0.1:8000/api/search?q=thai
```

Response:
```json
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "category": "string",
      "rating": number
    }
  ]
}
```

---

## Restaurant Detail

**GET** `/api/restaurants/{id}`

Example:
```
http://127.0.0.1:8000/api/restaurants/<id>
```

Response:
```json
{
  "id": "string",
  "title": "string",
  "category": "string",
  "rating": number,
  "address": "string",
  "phone": "string",
  "website": "string",
  "comments": [],
  "image_urls": []
}
```

---

## Add Comment

**POST** `/restaurants/{id}/comments`

Form fields:
- `author`
- `text`

---

## Notes

- Do NOT use Jinja templates
- Build frontend independently
- Use API responses only