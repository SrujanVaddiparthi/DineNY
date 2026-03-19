# Frontend Flow Notes

## Overall User Flow

### Search flow
User enters one or more of the following:

- text query
- latitude / longitude / radius
- min rating / max rating

Backend returns matching restaurants.

### Results flow
Frontend should display:

- restaurant title
- category
- rating
- address
- optional distance (for geo searches)
- map pins using latitude / longitude

### Detail flow
When user selects a restaurant, frontend should fetch:

- restaurant details
- primary image
- comments
- location data

Frontend can then display:

- restaurant information
- primary image
- extra images
- comments section
- single-location map with one pin

---

## Important Backend-Supported Behaviors

### Text search
The backend supports searching by:

- restaurant name
- cuisine/category
- address text

This means users can search things like:
- `thai`
- `halal`
- `broadway`
- `queens`

### Geo search
The backend supports searching by:
- latitude
- longitude
- radius

### Rating filter
The backend supports:
- `min_rating`
- `max_rating`

Frontend may later use:
- a slider
- two numeric boxes
- dropdowns

---

## Temporary Jinja App

There is already a working temporary backend-owned UI in:

- `app/templates/index.html`
- `app/templates/results.html`
- `app/templates/details.html`

This exists to:
- test backend flow
- validate API behavior
- provide a rough visual reference

Frontend should **not** build on top of Jinja templates directly.

---

## Current Suggested Frontend Pages

### 1. Search page
Inputs:
- text query
- latitude
- longitude
- radius
- min rating
- max rating

### 2. Results page
Show:
- list of restaurants
- result count
- map with pins

### 3. Detail page
Show:
- title
- category
- rating
- address
- phone
- website
- primary image
- other images
- comments
- single-location map

---

## Notes for Integration

- `primary_image_src` is now available for GridFS-backed image display
- detail endpoint already includes map-related fields
- search endpoint already includes coordinates for results map rendering