# Task Management

This section outlines the task creation, editing, viewing, and deletion process within the application.

## Task Creation
- Users can create tasks from their home page.
- A task includes a title, priority level, completion status, and is associated with a specific user.

## Task Editing
- Users can update the title, priority and completion status of tasks.

## Task Completing
- Users can complete a task, edit and complete buttons will be disabled and the task color will change.

## Task Deletion
- Users can delete tasks from their task list.

### Task Data
Tasks are stored in a MongoDB database with the following structure:

```json
{
  "_id": "12345",
  "title": "Finish documentation",
  "priority": "High",
  "username": "testuser",
  "completed": false
}
