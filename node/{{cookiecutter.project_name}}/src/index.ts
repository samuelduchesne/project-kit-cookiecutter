/**
 * Return a greeting for `name`.
 *
 * Replace this example with your library's public API.
 */
export function greet(name: string): string {
  if (name.trim() === "") {
    throw new RangeError("name must not be empty");
  }
  return `Hello, ${name}!`;
}
