# Example: Web Application Project

This example shows how to set up a web application project with the Agentic State Protocol.

## Project Type
- **Architecture**: Monolithic Application
- **Tech Stack**: JavaScript/TypeScript
- **Use Case**: Web applications, APIs, React/Vue/Next.js apps

## Initialization

```bash
# From the agentic-state-protocol root directory
python init_project.py

# When prompted:
# - Project name: "My Web App"
# - Tech stack: JavaScript/TypeScript (2)
# - Architecture: Monolithic Application (1)
```

## Resulting Structure

```
my_web_app/
├── docs/                      # Protocol documentation
├── src/my_web_app/            # Source code
│   ├── components/            # React components (add)
│   ├── pages/                 # Pages (add)
│   ├── api/                   # API routes (add)
│   ├── lib/                   # Utilities (add)
│   └── styles/                # Styles (add)
├── tests/
├── scripts/
├── configs/
├── .claude/
├── CLAUDE.md
├── package.json               # Add this
├── tsconfig.json              # Add this
└── README.md                  # Add this
```

## Recommended package.json

```json
{
  "name": "my-web-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write .",
    "test": "jest",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "jest": "^29.0.0"
  }
}
```

## Recommended tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*", "tests/**/*"],
  "exclude": ["node_modules"]
}
```

## Sample Component

```typescript
// src/components/Button.tsx
import { FC, ReactNode } from 'react';

interface ButtonProps {
  children: ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
}

export const Button: FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary'
}) => {
  const baseStyles = 'px-4 py-2 rounded font-medium';
  const variantStyles = {
    primary: 'bg-blue-500 text-white hover:bg-blue-600',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

## Workflow Example

```bash
# Start session
/boot

# Add a new page
/feature add-dashboard-page

# After implementing
/done

# Pre-commit checks
PRECOMMIT
# → Runs: eslint, prettier --check, tsc --noEmit, jest

# Save and commit
/save
```
