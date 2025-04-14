## 🖥️ User Interface Specification

This section outlines the structure and expected behavior of the user interface (UI) for the CBT system. The UI is designed with clarity, accessibility, and user guidance in mind to ensure a smooth and supportive mental health experience.

### 1. Overall Layout

- **Main View**: Split view with the conversation pane on the left and the agenda checklist on the right.
- **Top Navigation Bar**:
  - System branding/logo
  - User profile icon with sign out option
- **Footer (optional)**:
  - Link to emergency resources
  - Privacy policy

### 2. UI Components

#### a. Conversation Panel
- **Function**: Central chat interface for CBT conversation.
- **Features**:
  - Scrollable message history
  - User input field at the bottom
  - “Send” button to trigger message submission
  - Loading indicator when waiting for API response

#### b. Agenda Checklist
- **Function**: Tracks current CBT session items.
- **Features**:
  - List of agenda items with checkboxes
  - Items are checked automatically based on progress
  - Ability to mark items manually (developer/debug mode)

#### c. Modal/Popup Dialogs
- **Trigger Conditions**:
  - Self-harm or crisis keywords
  - Session completion or timeout
- **Content**:
  - Mental health resources and emergency contacts
  - Confirmation dialogs for sign-out or reset

### 3. Input Handling

- Messages are sent via the “Enter” key or “Send” button.
- Special tool triggers (e.g., self-harm detection, agenda updates) are activated on input recognition.
- UI is responsive to different screen sizes (mobile/tablet/desktop).

### 4. Accessibility

- Full keyboard navigation support
- Text contrast meets WCAG AA standards
- Alt-text for icons and screen reader compatibility

### 5. Error Handling & Feedback

- Clear error messages for failed API responses
- User feedback when session ends or messages aren’t delivered
- Graceful fallback if API is unreachable (retry, notify)
