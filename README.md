# Coeus

Coeus is a next-generation team collaboration platform designed to streamline project management and enhance team productivity. With features like real-time repository analysis, commit tracking, and seamless team collaboration, Coeus empowers teams to achieve more together.

## Features

- **Real-Time Code Repository Analysis**: Analyze your GitHub repositories in real-time to gain insights into your codebase.
- **Repository Commits Analysis**: Summarize and track commit changes with AI-powered insights.
- **Seamless Team Collaboration**: Collaborate with your team using an intuitive interface designed for efficiency.
- **Meeting Management**: Upload, view, and manage meetings with issue tracking and status indicators.
- **AI-Powered Summaries**: Leverage OpenAI's GPT models to summarize code files and commit diffs for better understanding and onboarding.

## Tech Stack

This project is built using the [T3 Stack](https://create.t3.gg/), which includes the following technologies:

- [Next.js](https://nextjs.org): React framework for building server-rendered and static web applications.
- [NextAuth.js](https://next-auth.js.org): Authentication for Next.js applications.
- [Prisma](https://prisma.io): ORM for database management.
- [Drizzle](https://orm.drizzle.team): Lightweight ORM for database queries.
- [Tailwind CSS](https://tailwindcss.com): Utility-first CSS framework for styling.
- [tRPC](https://trpc.io): End-to-end typesafe APIs.
- [OpenAI](https://openai.com): AI-powered features for summarization and embeddings.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/your-username/coeus.git
cd coeus
```

2. Install dependencies:

```bash
npm install
```

3. Set up environment variables:

Create a .env file in the root directory and add the following variables:

- NEXT_PUBLIC_APP_URL=http://localhost:3000
- OPENAI_KEY=your_openai_api_key
- DATABASE_URL=your_database_url

4. Set up the database:

Run the following commands to initialize the database:

```bash
npm run db:push
npm run db:generate
```

5. Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

## Usage

#### Dashboard

The dashboard provides an overview of your project, including:

1. **Invite Members**: Share a unique link to invite team members to your project.
2. **GitHub Integration**: View and interact with the linked GitHub repository.
3. **Team Members**: Display profile pictures of team members.
4. **Archive Project**: Archive the project with a confirmation dialog.
5. **Additional Features**: Includes components for asking questions, scheduling meetings, and viewing commit logs.

#### Create Project

To create a new project:

- Navigate to the "Create Project" page.
- Enter the project name, GitHub repository URL, and a GitHub personal access token.
= Submit the form to link the repository and create the project.


#### Meetings

Manage your meetings with the following features:

1. **View Meetings**: See a list of all meetings with their status and issue count.
2. **Delete Meetings**: Remove meetings with a single click.
3. **Upload Meetings**: Start by uploading a meeting to track issues and discussions.

## GitHub Integration

The application uses the GitHub API to:

- Fetch recent commits and summarize them using AI.
- Count repository files for credit checks.
- Load and index repository files for analysis.

## AI-Powered Features

1. **Commit Summarization**: Summarize git diffs to understand changes at a glance.
2. **Code Summarization**: Generate concise explanations of code files for onboarding and documentation.
3. **Embeddings**: Create vector embeddings for text summaries to enable advanced search and classification.

# Deployment

Follow the deployment guides for your preferred platform:

- Vercel
- Netlify
- Docker

The following scripts are available in the package.json file:

- npm run dev: Start the development server.
- npm run build: Build the application for production.
- npm run start: Start the production server.
- npm run lint: Run ESLint to check for code quality issues.
- npm run format:write: Format code using Prettier.
- npm run db:push: Push the Prisma schema to the database.
- npm run db:studio: Open Prisma Studio to manage the database.


## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the software, provided that the original copyright notice and license terms are included.

Start collaborating with your team today using Coeus! 🚀