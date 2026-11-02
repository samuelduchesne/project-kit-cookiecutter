import { describe, expect, it } from "vitest";

import { greet } from "../src/index.js";

describe("greet", () => {
  it("greets by name", () => {
    expect(greet("Ada")).toBe("Hello, Ada!");
  });

  it("rejects an empty name", () => {
    expect(() => greet(" ")).toThrow(RangeError);
  });
});
