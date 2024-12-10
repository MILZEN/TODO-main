# Tasks API

## Overview
This application allows users to create, view, edit, and delete tasks. The tasks are stored in the MongoDB database and are associated with the authenticated user.

## Task Management

Tasks are managed through the application’s front-end, and there is no separate API exposed for tasks.

### Add Task

Users can add tasks by filling out a form with the task's title, priority, and completion status.
Tasks are added via the web interface (no manual API calls are made). The data is sent to the back-end as part of a form submission.

- **Method**: `POST`
- **Route**: `/add/<username>`
- **Data**: 
    - `title` (string): The title of the task.
    - `priority` (string): The priority level of the task (e.g., High, Medium, Low).
    - `username` (string): The username of that user use.
    - `completed` (boolean): Whether the task is completed or not.


### Example

```json
{
  title: "New task!"
  priority: "medium"
  username: "Admin"
  completed: true
}
```

---

### View Tasks

Tasks associated with the authenticated user can be viewed on the user's home page.

* Method: `GET`
* Route: `/home/<username>`

---

### Edit Task

Users can edit their tasks, including the title and completion status.

* Method: `POST`
* Route: `/edit/<id>`
* Data:
    * `title` (string): The updated task title.
    * `completed` (boolean): Whether the task is completed or not.

---

### Delete Task

Users can delete tasks.

* Method: `DELETE`
* Route: `'/delete/<id>'`