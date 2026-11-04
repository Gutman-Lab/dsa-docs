# UI components (bdsa-react-components)

`bdsa-react-components` is GutmanLab's shared React component library for DSA
user interfaces. It provides viewer, browser, annotation, and authentication
components so each DSA front end does not reimplement them.

## Install

```bash
npm install bdsa-react-components
```

Peer dependencies:

```bash
npm install react@^18 react-dom@^18 openseadragon@^5 paper@^0.12
```

The package ships ESM, CommonJS, and TypeScript declarations. Import the
bundled stylesheet once in your application:

```tsx
import 'bdsa-react-components/styles.css'
```

## Authentication

### `DsaAuthManager`

Login and logout UI with a persisted session. It reads and writes the shared
`dsaAuthStore`, so other components pick up the same session.

```tsx
import { DsaAuthManager } from 'bdsa-react-components'

export function Header() {
  return <DsaAuthManager compact onAuthChange={(ok) => console.log(ok)} />
}
```

| Prop | Type | Default | Purpose |
| --- | --- | --- | --- |
| `onAuthChange` | `(isAuthenticated: boolean) => void` | — | Fires when login state changes |
| `allowServerConfig` | `boolean` | `true` | Let the user edit the DSA server URL |
| `compact` | `boolean` | `false` | Minimal toolbar layout |
| `className` | `string` | — | Custom container class |
| `externalLoginUrl` | `string` | — | Link to an external login page instead of the in-app modal |
| `embeddedApiLogin` | `boolean` | — | Add a username/password modal beside the external login link |

### Store and hooks

```tsx
import { dsaAuthStore, useDsaAuth, useDsaResolvedApi } from 'bdsa-react-components'

dsaAuthStore.updateConfig({ baseUrl: 'https://pub-data.bdsa.io' })

function Example() {
  const { authStatus, login, logout, getAuthHeaders } = useDsaAuth()
  const { apiBaseUrl, apiHeaders } = useDsaResolvedApi({})

  return (
    <p>
      {authStatus.isAuthenticated ? 'Signed in' : 'Signed out'} — {apiBaseUrl}
    </p>
  )
}
```

`useDsaAuth` returns `authStatus`, `login`, `logout`, `updateConfig`,
`getAuthHeaders`, and `getToken`. `useDsaResolvedApi` resolves the API root and
headers from the store, with optional `apiBaseUrl`, `apiHeaders`, and
`authToken` overrides.

## Browsing data

### `FolderBrowser`

A collection and folder tree backed by the DSA API. It reads the server URL and
token from `dsaAuthStore`; in `0.2.5` it has no `apiBaseUrl` prop.

```tsx
import { FolderBrowser } from 'bdsa-react-components'

<FolderBrowser
  onItemSelect={(item) => console.log(item)}
  rootId="collection-id"
  rootType="collection"
  persistExpansion
  persistSelection
/>
```

Selected props:

| Prop | Type | Purpose |
| --- | --- | --- |
| `rootId` + `rootType` | `string` + `'collection' \| 'folder'` | Show one subtree instead of every collection |
| `onItemSelect` | `(item: Item) => void` | Item row activated |
| `onResourceSelect` / `onSelectionChange` | `(resource) => void` | Collection, folder, or item selected |
| `onFolderOpen` | `(folder) => void` | Folder expanded |
| `allowedExtensions` | `string[]` | Filter items by extension |
| `itemFilter` | `(item) => boolean` | Custom item filter |
| `renderCollection` / `renderFolder` / `renderItem` | render props | Replace a row while keeping expansion behavior |
| `visualStyle` | `'modern' \| 'legacy'` | Panel styling |
| `persistExpansion` / `persistSelection` | `boolean` | Keep tree state across refresh |
| `scrollSelectedIntoView` | `boolean` (default `true`) | Scroll the selected row into view |
| `syntheticData` | object | Render static data for tests or Storybook |

### `ManifestBrowser`

Reads a JSON manifest and renders a browsable list. Props include
`manifestUrl` (default `/manifest.json`), `onItemSelect`, `selectedItemId`,
`defaultWidth`, and the usual `className`/`style`.

## Viewing slides

### `SlideViewer`

OpenSeadragon viewer with Paper.js annotation overlays.

```tsx
import { SlideViewer } from 'bdsa-react-components'

<SlideViewer
  imageInfo={{ dziUrl: 'https://host/api/v1/item/<id>/tiles/dzi.dzi' }}
  annotationIds={['annotation-id']}
  apiBaseUrl="https://host/api/v1"
  height="800px"
  onViewerReady={(viewer) => console.log(viewer)}
/>
```

`imageInfo` accepts either a `dziUrl` (recommended) or the manual fields
`imageId`, `width`, `height`, `tileWidth`, `levels`, and `baseUrl`.

Selected props:

| Prop | Type | Purpose |
| --- | --- | --- |
| `imageInfo` | `SlideImageInfo` | Required image descriptor |
| `annotations` | `AnnotationFeature[] \| FeatureCollection` | Inline annotations |
| `annotationIds` | `(string \| number)[]` | Fetch annotation documents from DSA |
| `apiBaseUrl` | `string` | API root including `/api/v1` |
| `height` | `string \| number` | Required container height |
| `onViewerReady` / `onToolkitReady` | callbacks | Access the OpenSeadragon viewer or annotation toolkit |
| `onAnnotationClick` | callback | Annotation selected |
| `showAnnotationControls` | `boolean` | Show the annotation controls panel |
| `showAnnotationInfo` | `boolean` | Show loaded-annotation details |
| `defaultAnnotationOpacity` | `number` | Base opacity (0–1) |
| `annotationOpacities` / `visibleAnnotations` | maps | Per-annotation state |
| `annotationCache` | cache or `null` | IndexedDB cache or disable caching |
| `tokenQueryParam` | `boolean` | Send the token as `?token=` for servers that require it |
| `onViewportChange` | callback | Normalized viewport bounds (0–1) |

Annotation limits default to 10,000 points per element and 100,000 points in
total. Elements above the per-element limit are skipped with a warning; the
total budget filters the largest annotations first.

### `AnnotationBrowser`, `AnnotationEditor`, and `SingleBoxSlideEditor`

- **`AnnotationBrowser`** lists an item's annotations and returns the selected
  one as GeoJSON (`itemId`, `onAnnotationSelect`, `defaultWidth`).
- **`AnnotationEditor`** wraps `SlideViewer` with a protocol-driven editing
  toolbar and exposes an imperative handle. Its prop and handle types are
  exported as `AnnotationEditorProps`, `AnnotationEditorConfig`,
  `AnnotationEditorHandle`, and related types.
- **`SingleBoxSlideEditor`** shows one slide-space box over a `SlideViewer` and
  reports `onBoxChange` / `onCommit`, with optional shape-edit and zoom-to-box
  controls.

## Thumbnails and protocols

- **`OSDThumbnailBrowser`** — paginated thumbnail browser backed by
  OpenSeadragon; the older name `FolderThumbnailBrowser` is a deprecated alias.
- **`ThumbnailGrid`** — grid of DSA item thumbnails with filtering and paging.
- **`ThumbnailViewer`** — one thumbnail with optional annotation overlay.
- **`ProtocolManager` / `ProtocolsTab`** — protocol definitions, storage, and
  DSA sync adapters; also exported as `ProtocolProvider`, `useProtocols`, and
  the schema helpers.

## Item helpers

The package exports `hasLargeImage`, `isAIModel`, `filterLargeImages`, and
`filterAIModels` from `utils/itemUtils`, plus the `Item` and `ItemWithMeta`
types. These are useful when filtering a `FolderBrowser` tree or building custom
rows.

## Example: sign in and browse

```tsx
import { useEffect } from 'react'
import {
  DsaAuthManager,
  FolderBrowser,
  dsaAuthStore,
} from 'bdsa-react-components'
import 'bdsa-react-components/styles.css'

export function App() {
  useEffect(() => {
    dsaAuthStore.updateConfig({ baseUrl: 'https://pub-data.bdsa.io' })
  }, [])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <DsaAuthManager compact />
      <div style={{ flex: 1, minHeight: 0 }}>
        <FolderBrowser persistExpansion />
      </div>
    </div>
  )
}
```

## Version notes

- `0.2.2` changed `AnnotationEditor` to look up an annotation by exact name
  instead of listing every annotation on the item.
- `0.2.5` is the version documented here. `Button` was removed in the `0.2`
  line; use your application's design system.
- The package's `docs/TO_DO.md` tracks internal backlog and is not a public API
  commitment.

## Getting help

Open an issue at
<https://github.com/Gutman-Lab/bdsa-react-components/issues>. For changes that
affect the DSA application, coordinate with the DSA front-end maintainers so the
library and the application move together.

??? note "Source and version"

    - **Package:** `bdsa-react-components` on npm
    - **Version documented here:** `0.2.5`
    - **Source:** <https://github.com/Gutman-Lab/bdsa-react-components>
    - **License:** Apache-2.0

    This reference was written against the published `0.2.5` package's type
    declarations and the repository at commit
    [`399c2b3`](https://github.com/Gutman-Lab/bdsa-react-components/commit/399c2b3)
    on 2026-11-01. The components were **not rendered in a live DSA
    application** for this page. The package's own `README.md` and
    `docs/API.md` still describe removed exports (`Card`, `AnnotationManager`)
    and a `FolderBrowser` `apiBaseUrl` prop; the `0.2.5` type declarations are
    authoritative where they disagree.
