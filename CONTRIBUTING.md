# 🛠️ CONTRIBUTING GUIDELINES – ElevoraAI

Welcome to **ElevoraAI**! 🚀  

We’re beyond thrilled to have you here and excited to see your ideas come to life!  
**ElevoraAI** is an open-source initiative built to empower **students, developers, and professionals** through **intelligent learning tools, AI-driven career growth, and collaborative development**. 🌍✨  

> 💡 **Every single contribution counts!** From fixing a typo to building a new feature — you’re helping shape the future of learning.  

Please make sure to read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). 💖  
For architecture, setup, and onboarding — check [.project-docs/LEARN.md](.project-docs/LEARN.md) for a complete contributor roadmap. 🗺️

---

## 📌 Contribution Philosophy

Contributing to open source means **collaboration, respect, and growth**.  
Here’s what you can contribute to:

- 🐞 **Bug Fixes**
- ✨ **New Features / Modules**
- 🎨 **UI/UX Enhancements**
- 📚 **Documentation Updates**
- 🧪 **Test Case Additions**
- 🤖 **AI Dataset / Prompt Improvements**
- 🔒 **Security & Performance Optimizations**

> 🧭 Whether you’re a beginner or a pro — ElevoraAI is the perfect space to learn, build, and grow together.

---

## 🚀 Quick Start — Step-by-Step Guide

### 1. 🌟 Star the Repository

Show your support by starring ⭐ the repo. It motivates contributors!

### 2. 🍴 Fork the Repository

Click on the **Fork** button in the top-right corner of this repository.

### 3. 📥 Clone Your Fork

```bash
git clone https://github.com/<your-username>/elevora-ai.git
cd elevora-ai
````

### 4. 📦 Install Dependencies

The project consists of two parts — **Client (Frontend)** and **Server (Backend)**.

**Frontend Setup (React + Vite):**

```bash
cd ElevoraAI/Client
npm install
```

**Backend Setup (Node.js + Express):**

```bash
cd ElevoraAI/Server
npm install
```

---

### 5. ⚙️ Run in Development Mode

Run both client and server in separate terminals.

**Backend:**

```bash
cd ElevoraAI/Server
node index.js
```

**Frontend:**

```bash
cd ElevoraAI/Client
npm run dev
```

💡 The app usually runs at:

* Frontend → `http://localhost:5173`
* Backend → `http://localhost:5000` (or as defined in `.env`)

---

### 6. 🌍 Environment Configuration (Optional)

If needed, configure your `.env` file:

```bash
cd ElevoraAI/Server
cp .env.sample .env
```

Edit the `.env` file with your database keys, tokens, etc.

---

## ⚠️ IMPORTANT WARNING — Before You Push!

> 💡 **Always ensure you’re on the correct branch before committing or pushing code.**

### 🔴 Commands to Follow:

```bash
git checkout <branch-name>       # 🔁 Switch to your assigned branch
git pull origin <branch-name>    # ⬇️ Pull latest updates
git add .                        # ➕ Stage your changes
git commit -m "✨ Your clear message here"  # 💬 Commit with clarity
git push origin <branch-name>    # 🚀 Push safely
```

🧠 **Tip:** Always double-check the branch name before pushing — it saves everyone from messy merge conflicts! ⚡

---

## 🧭 Syncing Your Fork with the Upstream Repo

To stay updated with the latest main branch:

```bash
git remote add upstream https://github.com/abhisek2004/elevora-ai.git
git pull upstream main
git push origin main
```

---

## 🌿 Branch & Commit Rules

* ✅ Use **meaningful commit messages** (e.g., `fix: UI glitch in dashboard cards`)
* ✅ Keep changes small and focused
* ✅ Run your code before submitting PR
* ✅ Avoid committing node_modules or build files

---

## 🔧 Pull Request (PR) Process

1. Fork → Clone → Work on changes
2. Commit using meaningful messages
3. Push changes to your branch
4. Create a **Pull Request to the `main` branch** of [ElevoraAI](https://github.com/abhisek2004/elevora-ai)
5. Add proper description, screenshots (if UI), and related issue numbers (`Closes #issue_no`)

> 🧩 PRs without proper descriptions may be delayed for review.

---

## 🧩 What Can You Contribute?

| Area              | You Can Contribute                                         |
| ----------------- | ---------------------------------------------------------- |
| 🖥️ Frontend      | Responsive design, dark mode, new components, animations   |
| ⚙️ Backend        | API enhancements, authentication, performance optimization |
| 🤖 AI Engine      | Smart recommendations, chatbot logic, dataset curation     |
| 🗂️ Documentation | Guides, tutorials, GIFs, flow diagrams                     |
| 🧩 Tools          | Resume Builder, Project Tracker, Mentor Dashboard modules  |

💥 You can also propose **new modules, gamification features, or API integrations**!

---

## 🧠 Issue Reporting Guide

1. Visit [Issues](https://github.com/abhisek2004/elevora-ai/issues)
2. Check if the issue already exists
3. Use clear titles & descriptions
4. Add labels (`bug`, `feature`, `good first issue`)
5. Wait for assignment before you start coding

---

## 🤝 Community & Mentorship

We believe in **collaboration over competition**. 💪
Get guidance, discuss your ideas, and connect with mentors in our **ElevoraAI Community Discussions** or Discord.
You’ll gain hands-on mentorship, feedback, and growth opportunities.

---

## 💡 Helpful Resources

* 📘 [How to Fork a Repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
* 🔄 [How to Create a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
* 🧭 [GitHub Docs](https://docs.github.com/en)
* 💬 Join ElevoraAI Discussions or Discord (coming soon)

---

## 👨‍💻 Project Owner & Maintainer

<<<<<<< HEAD
**Mr Alpha**
=======
**Abhisek Panda**
>>>>>>> 6bb7a38405a5539730eea1d48749b7c3e992c2c5
📧 [officialElevoraAI@gmail.com](mailto:officialElevoraAI@gmail.com)
🌐 [GitHub: abhisek2004](https://github.com/abhisek2004)

---

## 💖 Thank You!

Thanks a ton for taking the time to contribute!
Your efforts — whether a small fix or a big feature — help us empower developers and learners across the world. 🌏

> 🧠 *Let’s build the future of smart learning together — one meaningful commit at a time.*

**Happy Coding! 🚀💻✨**

---


