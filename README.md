# pkl-whispercpp

Typed Pkl module for rendering a CUDA-enabled [whisper.cpp](https://github.com/ggml-org/whisper.cpp) Docker Compose deployment.

It renders a one-shot model initializer and a local transcription service. The initializer downloads the selected GGML Whisper model into a persistent host directory; the service waits for it, mounts it read-only, and exposes `/inference` only on the configured host address.

The image repository, upstream image tag, and immutable digest are separate settings. The official CUDA image uses the `main-cuda` channel; its registry does not publish matching Whisper.cpp release-version tags. Renovate updates the digest while the declared tag stays visible.

## Example

```pkl
amends "package://github.com/faisal-memon/pkl-whispercpp@0.1.0#/Compose.pkl"

import "package://github.com/faisal-memon/pkl-whispercpp@0.1.0#/Whispercpp.pkl"

settings = new Whispercpp {
  model = "medium"
  modelDirectory = "/var/lib/whispercpp/models"
  hostIp = "127.0.0.1"
}
```

Render and validate the included example:

```sh
make validate
```

The generated service requires Docker's NVIDIA Container Toolkit and the official CUDA whisper.cpp image, pinned by digest for reproducible deployments. Renovate updates that digest as upstream publishes builds. The transcription API accepts multipart audio at `POST /inference`; see the [upstream server documentation](https://github.com/ggml-org/whisper.cpp/tree/master/examples/server) for its request format.
