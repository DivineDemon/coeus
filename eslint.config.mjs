import { defineConfig } from "eslint-define-config";

export default defineConfig({
  extends: ["next/core-web-vitals", "next/typescript", "prettier"],
  plugins: ["check-file", "n"],
  rules: {
    "no-console": ["error"],
    "eqeqeq": ["error"],
    "prefer-arrow-callback": ["error"],
    "prefer-template": ["error"],
    semi: ["error"],
    quotes: ["error", "double"],
    "n/no-process-env": ["error"],
    "check-file/filename-naming-convention": [
      "error",
      {
        "**/*.{ts,tsx}": "KEBAB_CASE",
      },
      {
        ignoreMiddleExtensions: true,
      },
    ],
    "check-file/folder-naming-convention": [
      "error",
      {
        "src/**/!^[.*": "KEBAB_CASE",
      },
    ],
  },
});
