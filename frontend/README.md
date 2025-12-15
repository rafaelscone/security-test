# Todo List App

A modern todo list application built with Nuxt.js (SPA mode) and Tailwind CSS.

## Features

- ✅ Client-side rendering (SPA mode)
- 🎨 Beautiful UI with Tailwind CSS
- 📝 Create, read, update, and delete todos
- ✔️ Toggle todo completion status
- 🔍 Filter todos by status (All, Active, Completed)
- 📊 Real-time statistics

## Prerequisites

- Node.js (v18 or higher)
- Backend API running on `http://localhost:8000`

## API Endpoints Expected

The app expects the following API endpoints:

- `GET /todos` - Get all todos
- `POST /todos` - Create a new todo
- `PUT /todos/:id` - Update a todo
- `DELETE /todos/:id` - Delete a todo

### Todo JSON Format

```json
{
  "title": "string",
  "description": "string",
  "completed": true
}
```

## Installation

```bash
npm install
```

## Development

Start the development server on `http://localhost:3000`:

```bash
npm run dev
```

## Production

Build the application for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

Generate static site:

```bash
npm run generate
```

## Configuration

The API base URL can be configured in [nuxt.config.ts](nuxt.config.ts):

```typescript
runtimeConfig: {
  public: {
    apiBase: 'http://localhost:8000'
  }
}
```

## Project Structure

```
todo-app/
├── pages/
│   └── index.vue          # Main todo list page
├── app.vue                # Root component
├── nuxt.config.ts         # Nuxt configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── package.json           # Dependencies and scripts
```
