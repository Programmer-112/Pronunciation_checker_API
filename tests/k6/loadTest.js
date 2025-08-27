import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
    scenarios: {
        // Normal traffic: typical users scoring audio
        normal_traffic: {
            executor: "constant-vus",
            vus: 10,
            duration: "1m",
            exec: "scoreAudio",
        },
        // Health checks
        health_check: {
            executor: "constant-vus",
            vus: 5,
            duration: "1m",
            exec: "health",
        },
        // Spike scenario: sudden surge in audio uploads
        spike_test: {
            executor: "ramping-vus",
            startVUs: 0,
            stages: [
                { duration: "10s", target: 20 }, // ramp up
                { duration: "10s", target: 20 }, // hold peak
                { duration: "10s", target: 0 },  // ramp down
            ],
            exec: "scoreAudio",
        },
        // Stress test: continuous requests without sleep
        stress_test: {
            executor: "constant-vus",
            vus: 5,
            duration: "1m",
            exec: "scoreAudioNoSleep",
        },
    },
};
let payload = {
        target: "i love you",
        file: http.file(open("../audio/iloveyou.webm", "b"), "iloveyou.webm", "audio/webm"),
    };

const scoreRoute = "http://127.0.0.1:8000/api/v1/score/"
const healthRoute = "http://127.0.0.1:8000/health"
// Health endpoint
export function health() {
    let res = http.get(healthRoute);
    check(res, { "health 200": (r) => r.status === 200 });
    sleep(1); // simulate human think time
}

// Score-audio endpoint with normal pacing
export function scoreAudio() {
   
    let res = http.post(scoreRoute, payload);
    check(res, { "status 200": (r) => r.status === 200 });
    sleep(1); // human-like pacing
}

// Score-audio endpoint without sleep for stress testing
export function scoreAudioNoSleep() {
    
    let res = http.post(scoreRoute, payload);
    check(res, { "status 200": (r) => r.status === 200 });
    // no sleep, continuous load
}
