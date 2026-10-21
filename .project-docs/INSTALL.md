# 📦 INSTALL.md – Setup Guide for DevElevate

Welcome to **DevElevate – Your Smart Learning & Career Hub** 🚀
This guide walks you through **cloning**, **installing dependencies**, and **running the project locally** using **Vite**, **React (TypeScript)**, **Tailwind CSS**, and **Node.js**.
Please ensure you follow the proper **folder structure** to avoid bugs or broken references.

---

## ✅ Prerequisites

Before you begin, make sure you have the following installed:

| Tool          | Version | Download Link                                        |
| ------------- | ------- | ---------------------------------------------------- |
| Node.js       | ≥ 18.x  | [Download Node.js](https://nodejs.org/)              |
| Git           | ≥ 2.x   | [Download Git](https://git-scm.com/)                 |
| VS Code       | Latest  | [Download VS Code](https://code.visualstudio.com/)   |
| MongoDB Atlas | –       | [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) |

---

## 🔁 Clone the Repository

```bash
git clone https://github.com/abhisek2004/Dev-Elevate.git
cd Dev-Elevate
```

---

## 📁 Project Structure Overview

Here's the current recommended folder structure:

```
DevElevate/
│
├── .github/               → GitHub metadata and workflows
├── DevElevate/            → Primary app source folder
│   ├── Admin/             → Admin dashboard and controls
│   ├── Auth/              → Login, Register, Auth layout
│   ├── Chatbot/           → AI chatbot integration (GPT-4)
│   ├── Dashboard/         → User dashboard & home cards
│   ├── Layout/            → Header, sidebar, routes
│   ├── LearningHub/       → Courses, roadmaps, notes
│   ├── Legal/             → Code of conduct, license, terms
│   ├── PlacementPrep/     → HR prep, resources, jobs
│   ├── Profile/           → Profile management, settings
│   ├── ResumeBuilder/     → Resume, cover letter, GPT-based tips
│   └── TechFeed/          → News, YouTube, Hackathons
│
├── src/                   → App entry point
│   ├── components/        → Shared UI components
│   ├── contexts/          → GlobalContext, AuthContext
│   ├── App.tsx            → Main application shell
│   ├── index.tsx          → Root renderer
│   └── main.tsx           → Mounting and routing logic
│
├── dist/                  → Production build output (after `npm run build`)
├── .bolt/                 → Optional: bolt or runtime configs
├── .gitignore             → Git ignored files
├── vite.config.ts         → Vite build config
├── tailwind.config.js     → Tailwind setup
├── postcss.config.js      → PostCSS setup
├── tsconfig.json          → TS global config
├── tsconfig.app.json      → App-specific TS config
├── package.json           → Project dependencies and scripts
├── README.md              → Project overview
├── LICENSE                → Project license
├── CODE_OF_CONDUCT.md     → Code of conduct
├── CONTRIBUTING.md        → How to contribute
├── ROADMAP.md             → Feature roadmap
├── SECURITY.md            → Security policy
├── AUTHORS                → Project author info
```

---

## 📦 Install Dependencies

```bash
npm install
```

Make sure you are in the **root folder** where the `package.json` file exists.

---

## 🚀 Run the Project

Use Vite's dev server to run the project locally:

```bash
npm run dev
```

After the app starts, navigate to:

```
http://localhost:5173/
```

---

## 🧪 Initial State & Testing

### ⚠️ **Note**:

- As of the current base UI state, the **login** / **sign-up** page is for demonstration only.
- There is **no real database connection yet**. Your data is stored in **browser cache/local memory**.
- After registration (user/admin), you'll be able to see respective dashboard UIs.
- Once the backend is integrated, we’ll connect this with **MongoDB Atlas** and **JWT-based auth**.

---

## 🔐 MongoDB Atlas Setup (Planned)

> A complete `.env` template and MongoDB cluster connection URL will be shared once the contribution opens.

---

## 💡 Useful NPM Scripts

```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "lint": "eslint . --ext .js,.jsx,.ts,.tsx"
}
```

---

## 🧪 Testing

Manual testing is being done during this stage. Automated testing framework (e.g., Vitest or Jest) will be integrated soon.

---

## 📥 Need Help?

Feel free to reach out:

- 💬 [GitHub Discussions](https://github.com/abhisek2004/Dev-Elevate/discussions)
- 📧 [officialdevelevate@gmail.com](mailto:officialdevelevate@gmail.com)
<<<<<<< HEAD
- 🧑‍💻 Project Maintainer: Mr Alpha
=======
- 🧑‍💻 Project Maintainer: Abhisek Panda
>>>>>>> 6bb7a38405a5539730eea1d48749b7c3e992c2c5

---

## ✅ Next Steps After Setup

1. Explore the folder structure
2. Make UI changes or add new sections under `DevElevate/`
3. Raise issues or create PRs with improvements
4. Join our Discord/community chat (coming soon)

---

Thank you for installing and setting up **DevElevate** locally! 💻
Now let’s build the smartest education & career platform together. 🚀
