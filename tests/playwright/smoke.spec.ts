import { test, expect } from '@playwright/test';

test.beforeEach(async ({ request }) => {
  const reset = await request.post('/lab/reset');
  expect(reset.ok()).toBeTruthy();
});

test('service root links to Systems collection', async ({ request }) => {
  const response = await request.get('/redfish/v1');
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body.Systems['@odata.id']).toBe('/redfish/v1/Systems');
});

test('ComputerSystem resource looks Redfish-like', async ({ request }) => {
  const response = await request.get('/redfish/v1/Systems/1');
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body['@odata.type']).toContain('ComputerSystem');
  expect(body.Manufacturer).toBe('HPE');
});
