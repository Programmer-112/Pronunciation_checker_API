import http from "k6/http";
import { check } from "k6";

export let options = {
  scenarios: {
    // Stress test: continuous requests without sleep
    stress_test: {
      executor: "constant-vus",
      vus: 30,
      duration: "1m",
      exec: "scoreAudioNoSleep",
    },
  },
};

const longAudioPayload = {
  target: `Turtle shells are made mostly of bone the upper part is the domed carapace 
        while the underside is the flatter plastron or belly plate`,
  file: http.file(
    open("../audio/turtle.webm", "b"),
    "turtle.webm",
    "audio/webm"
  ),
};

const scoreRoute = "http://127.0.0.1:5000/api/v1/score/";

// Score-audio endpoint without sleep for stress testing
export function scoreAudioNoSleep() {
  let res = http.post(scoreRoute, longAudioPayload);
  check(res, { "status 200": (r) => r.status === 200 });
  // no sleep, continuous load
}
