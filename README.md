# pkl-whispercpp

Typed Pkl module for rendering a CUDA-enabled [whisper.cpp](https://github.com/ggml-org/whisper.cpp) Docker Compose deployment.

It renders a one-shot model initializer and a transcription service. The initializer downloads the selected GGML Whisper model into a persistent host directory; the service waits for it, mounts it read-only, and can either publish `/inference` on the host or attach to a pre-existing external Docker network for internal callers.

The image repository and pinned version are separate settings. The version contains both the `main-cuda` tag and immutable digest. Renovate updates the pinned image version as upstream publishes builds.

## Example

```pkl
amends "package://github.com/faisal-memon/pkl-whispercpp@0.1.0#/src/render/Compose.pkl"

import "package://github.com/faisal-memon/pkl-whispercpp@0.1.0#/Whispercpp.pkl"
import "package://github.com/faisal-memon/pkl-whispercpp@0.1.0#/DockerCompose.pkl"

config {
  whispercpp = new Whispercpp {
    model = "medium"
  }
  hostModelDirectory = "/var/lib/whispercpp/models"
  hostPublishing = new DockerCompose.HostPublishing {}
}
```

For an internal service, leave `hostPublishing` unset and
`externalNetworkName = "ai_net"`. The generated service then listens on its
container port without competing for a host port, and other containers on the
external network can reach it as `whispercpp:8080`.

Render and validate the included example:

```sh
make validate
```

The generated service requires Docker's NVIDIA Container Toolkit and the official CUDA whisper.cpp image, pinned by digest for reproducible deployments. Renovate updates that pinned version as upstream publishes builds. The transcription API accepts multipart audio at `POST /inference`; see the [upstream server documentation](https://github.com/ggml-org/whisper.cpp/tree/master/examples/server) for its request format.
