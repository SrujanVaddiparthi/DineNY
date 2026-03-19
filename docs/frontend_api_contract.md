# Frontend API Contract

Frontend should interact with the backend through the API endpoints below.

---

## 1. Search Endpoint

**GET** `/api/search`

### Supported query parameters

- `q` → optional text query  
- `lat` → optional latitude  
- `lon` → optional longitude  
- `radius` → optional radius in meters  
- `min_rating` → optional minimum rating  
- `max_rating` → optional maximum rating  

### Example requests

**Text-only search**
```
/api/search?q=thai
```

**Geo-only search**
```
/api/search?lat=40.7128&lon=-74.0060&radius=2000
```

**Text + geo + rating**
```
/api/search?q=vegan&lat=40.7128&lon=-74.0060&radius=3000&min_rating=4.0
```

### Response shape

```json
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "category": "string",
      "rating": 4.5,
      "address": "string",
      "has_image": true,
      "latitude": 40.7128,
      "longitude": -74.0060,
      "distance_meters": 312.45
    }
  ]
}
```

### Notes

- `distance_meters` will only appear for geo-based searches
- search works against restaurant name, cuisine/category, and address text
- street-name search is supported because address data is included in searchable text

---

## 2. Restaurant Detail Endpoint

**GET** `/api/restaurants/{id}`

### Example request

```
/api/restaurants/69bb45ece5023977a97b4eda
```

### Response shape

```json
{
  "id": "string",
  "title": "string",
  "category": "string",
  "rating": 5,
  "website": "string",
  "phone": "string",
  "address": "string",
  "categories": ["string"],
  "image_urls": [
    {
      "thumbnail": "string",
      "title": "string"
    }
  ],
  "primary_image_gridfs_id": "string",
  "primary_image_src": "/api/images/<file_id>",
  "latitude": 40.5761148,
  "longitude": -73.9860024,
  "location": {
    "type": "Point",
    "coordinates": [-73.9860024, 40.5761148]
  },
  "comments": [
    {
      "author": "string",
      "text": "string",
      "created_at": "string"
    }
  ]
}
```

### Notes

- `primary_image_src` should be used as the main image source
- if needed, frontend can fall back to `image_urls[0].thumbnail`
- `latitude`, `longitude`, and `location` are provided for detail-page map rendering

---

## 3. Image Endpoint

**GET** `/api/images/{file_id}`

### Purpose

Serves an image stored in MongoDB GridFS.

### Example request

```
/api/images/69bc78be898521ec86b75275
```

### Notes

- this endpoint returns image bytes, not JSON
- frontend can directly use it in an `<img src="...">`

---

## 4. Comment Submission

**POST** `/restaurants/{id}/comments`

### Form fields

- `author`
- `text`

### Notes

- current implementation is form-based because the Jinja prototype uses HTML forms
- frontend can either submit a form POST or later we can expose a JSON comment endpoint if needed

---

## Frontend Guidance

Frontend team should:

- build independently from the Jinja templates
- use the API endpoints above as the contract
- treat `templates/` only as a temporary flow/reference implementation