import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App", () => {
    it("renders the button", () => {
        render(<App />);
        expect(
            screen.getByRole("button", { name: /insert the app here/i })
        ).toBeInTheDocument();
    });
});
