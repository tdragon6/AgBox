export default {};

export function isReportMode(): boolean {
  return process.env.REPORT === 'true';
}
