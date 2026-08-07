// dmn-js ships no TypeScript declarations (unlike bpmn-js). The read-only Viewer
// is dynamically imported and cast to a local interface in DmnArtifact.tsx; this
// shim just satisfies module resolution so the import isn't an implicit-any error.
declare module 'dmn-js/lib/Viewer';
