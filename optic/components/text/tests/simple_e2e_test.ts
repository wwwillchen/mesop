import { test, expect } from "@playwright/test";

test("test", async ({ page }) => {
  await page.goto("/components/text/tests/fixtures/simple");
  expect(await page.getByText("Hello, world!").textContent()).toContain(
    "Hello, world!",
  );
});
