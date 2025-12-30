import http from 'k6/http';
import { check, sleep } from 'k6';

// Сценарии
export const options = {
  scenarios: {
    // 1. iterations - для top-academy
    top_academy: {
      executor: 'per-vu-iterations',
      vus: 1,
      iterations: 15,
      exec: 'testTopAcademy',
    },
    // 2. постоянная нагрузка - для fojin.tech
    fojin: {
      executor: 'constant-vus',
      vus: 5,
      duration: '20s',
      exec: 'testFojin',
    },
    // 3. ступенчатая нагрузка - для career.habr.com
    habr_career: {
      executor: 'ramping-vus',
      stages: [
        { duration: '10s', target: 5 },
        { duration: '15s', target: 10 },
        { duration: '10s', target: 0 },
      ],
      exec: 'testHabrCareer',
    },
    // 4. Постоянная нагрузка - для grafana.com
    grafana: {
      executor: 'constant-vus',
      vus: 100,
      duration: '30s',
      exec: 'testGrafana',
    },
    // 5. Постоянная нагрузка - для selenium.dev
    selenium: {
      executor: 'constant-vus',
      vus: 30,
      duration: '15s',
      exec: 'testSelenium',
    },
  },
};

//Функции для каждого сценария

export function testTopAcademy() {
  const res = http.get('https://taganrog.top-academy.ru/');
  check(res, { 'top-academy status 200': (r) => r.status === 200 });
  sleep(1);
}

export function testFojin() {
  const res = http.get('https://fojin.tech/');
  check(res, { 'fojin status 200': (r) => r.status === 200 });
  sleep(1.5);
}

export function testHabrCareer() {
  const res = http.get('https://career.habr.com/');
  check(res, { 'habr career status 200': (r) => r.status === 200 });
  sleep(1);
}

export function testGrafana() {
  const res = http.get('https://grafana.com/');
  check(res, { 'grafana status 200': (r) => r.status === 200 });
  sleep(0.1); 
}

export function testSelenium() {
  const res = http.get('https://www.selenium.dev/');
  check(res, {
    'selenium status 200': (r) => r.status === 200  });
  sleep(1);
}