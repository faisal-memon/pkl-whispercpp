# pkl-whispercpp

Typed Pkl module for rendering a CUDA-enabled [whisper.cpp](https://github.com/ggml-org/whisper.cpp) Docker Compose deployment.

It renders a one-shot model initializer and a local transcription service. The initializer downloads the selected GGML Whisper model into a persistent host directory; the service waits for it, mounts it read-only, and exposes `/inference` only on the configured host address.

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

The generated service requires Docker's NVIDIA Container Toolkit and the official `main-cuda` whisper.cpp image. The transcription API accepts multipart audio at `POST /inference`; see the [upstream server documentation](https://github.com/ggml-org/whisper.cpp/tree/master/examples/server) for its request format.
