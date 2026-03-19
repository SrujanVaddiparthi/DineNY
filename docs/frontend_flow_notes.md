# Frontend Flow Notes

## Search Flow

User enters search  
→ GET `/api/search?q=`  
→ Display results  
→ User clicks restaurant  

---

## Detail Flow

User clicks restaurant  
→ GET `/api/restaurants/{id}`  
→ Render:
- title
- rating
- images
- comments  

---

## Comment Flow

User submits comment  
→ POST `/restaurants/{id}/comments`  
→ Reload page  
→ New comment appears  

---

## Important Notes

- Backend HTML pages are only reference
- Frontend should be built independently
- Follow API contract strictly