# Fault Injection
## 1. Fault Type
### Network
| fault_name             | tool        | description       |
|:-----------------------|:------------|:------------------|
| pod-http-request-delay | chaos-mesh  | src=all, dest=pod |
| pod-http-request-abort | chaos-mesh  | src=all, dest=pod |
| svc-http-request-delay | chaos-mesh  | src=all, dest=svc |
| svc-http-request-abort | chaos-mesh  | src=all, dest=svc |
| pod-pod-network-delay  | chaos-blade | src=pod, dest=pod |
| pod-pod-network-drop   | chaos-blade | src=pod, dest=pod |
| svc-svc-network-delay  | chaos-blade | src=svc, dest=svc |
| svc-svc-network-drop   | chaos-blade | src=svc, dest=svc |

### API
| fault_name    | tool        | description   |
|:--------------|:------------|:--------------|
| api-delay     | chaos-blade | api delay     |
| api-exception | chaos-blade | api exception |

### CPU

### Memory

## 2. Service
All services and their ports:

| service                      | port  |
|:-----------------------------|:------|
| ts-admin-basic-info-service  | 18767 |
| ts-admin-order-service       | 16112 |
| ts-admin-route-service       | 16113 |
| ts-admin-travel-service      | 16114 |
| ts-admin-user-service        | 16115 |
| ts-assurance-service         | 18888 |
| ts-auth-service              | 12349 |
| ts-basic-service             | 15680 |
| ts-cancel-service            | 18885 |
| ts-config-service            | 15679 |
| ts-consign-price-service     | 16110 |
| ts-consign-service           | 16111 |
| ts-contacts-service          | 12347 |
| ts-execute-service           | 12386 |
| ts-food-service              | 18856 |
| ts-gateway-service           | 18888 |
| ts-inside-payment-service    | 18673 |
| ts-order-other-service       | 12032 |
| ts-order-service             | 12031 |
| ts-payment-service           | 19001 |
| ts-preserve-other-service    | 14569 |
| ts-preserve-service          | 14568 |
| ts-price-service             | 16579 |
| ts-rebook-service            | 18886 |
| ts-route-plan-service        | 14578 |
| ts-route-service             | 11178 |
| ts-seat-service              | 18898 |
| ts-security-service          | 11188 |
| ts-station-service           | 12345 |
| ts-train-food-service        | 19999 |
| ts-train-service             | 14567 |
| ts-travel-plan-service       | 14322 |
| ts-travel-service            | 12346 |
| ts-travel2-service           | 16346 |
| ts-user-service              | 12346 |
| ts-verification-code-service | 15678 |
