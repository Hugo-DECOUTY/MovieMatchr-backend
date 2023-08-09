# MovieMatchr API - Documentation

<!--

## Table of Contents
- [Account](#account)
  - [Get account](#get-account)
  - [Post create new user](#post-create-new-user)
- [Licences](#licences)
  - [Get licences from order](#get-licences-from-order)
  - [Patch user licence](#patch-user-licence)
- [Orders](#orders)
  - [Get orders](#get-orders)
  - [Get order](#get-order)
  - [Get order users](#get-order-users)
  - [Get order informations](#get-order-informations)
  - [Get order attachement](#get-order-attachement)
  - [Post order](#post-order)
  - [Post order attachement](#post-order-attachement)
  - [Patch order](#patch-order)
  - [Patch order billing type](#patch-order-billing-type)
  - [Patch order sharing authorization](#patch-order-sharing-authorization)
  - [Delete order](#delete-order)
- [Sellers](#sellers)
  - [Get sellers](#get-sellers)
  - [Get seller](#get-seller)
- [Tickets](#tickets)
  - [Get tickets](#get-tickets)
  - [Get ticket](#get-ticket)
  - [Post ticket](#post-ticket)
  - [Patch ticket](#patch-ticket)
  - [Patch process ticket](#patch-process-ticket)
  - [Delete ticket](#delete-ticket)

--------------------------------------------------

## Account

### Get account

#### Request
```http
GET /account/{account_id}
```

##### Path parameters
- account_id : uuid (keycloak user's id)

#### Response

##### 200 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "email": "john.doe@test.com",
    "first_name": "John",
    "last_name": "Doe",
}
```

###### Schema
```json
{
    "id": uuid,
    "email": string,
    "first_name": string,
    "last_name": string,
}
```

##### 403 - Forbidden

##### 404 - user-not-found

#### Description
> Return account's informations.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return account's informations
> - LOCAL_ADMIN: 200 and return account's informations

---

### Post create new user

#### Request
```http
POST /account/new_user
```

#### Body
```json
{
    "id_order": "00000000-0000-0000-0000-000000000000",
    "type": 0,
    "body": {
        "type_2fa": 0,
        "licence_type": 0,
        "serial_number": "YB2307900E",
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@test.com",
    }
}
```

###### Schema
```json
{
    "id_order": uuid,
    "type": integer,
    "body": {
        "type_2fa": integer,
        "licence_type": integer,
        "serial_number": string (necessary if type == 0),
        "firstname": string,
        "lastname": string,
        "email": string,
    }
}
```

#### Response

##### 201 - OK
```json
{
  "message": "New user created"
}
```

###### Schema
```json
{
  "message": string
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - order-not-found

##### 404 - licence-not-found

##### 403 - licence-already-used

##### 403 - user-already-exists

##### 500 - user-creation-failed

#### Description
> Create a new user.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 201 and return message
> - LOCAL_ADMIN: 201 and return message

---

## Licences

### Get licences from order

#### Request
```http
GET /licences/{id_order}
```

##### Path parameters
- id_order : uuid

#### Response

##### 200 - OK
```json
[
  {
    "id": "00000000-0000-0000-0000-000000000000",
    "licence_type": 0,
    "serial_number": "YB2307900E",
    "id_order": "00000000-0000-0000-0000-000000000000",
    "id_user": "00000000-0000-0000-0000-000000000000",
    "nb_recording_analysed": 0,
    "demo_flag": false,
    "active": true,
  }
]
```

###### Schema
```json
[
  {
    "id": uuid,
    "licence_type": integer,
    "serial_number": string,
    "id_order": uuid,
    "id_user": uuid,
    "nb_recording_analysed": integer,
    "demo_flag": boolean,
    "active": boolean,
  }
]
```

##### 403 - Forbidden

##### 404 - order-not-found

##### 403 - you-do-not-own-this-order

#### Description
> Return all licences linked to an order.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return all licences linked to an order
> - LOCAL_ADMIN: 200 and return all licences linked to an order

---

### Patch user licence

#### Request
```http
PATCH /licences/{id_licence}/user
```

##### Path parameters
- id_licence : uuid

#### Response

##### 204 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "licence_type": 0,
    "serial_number": "YB2307900E",
    "id_order": "00000000-0000-0000-0000-000000000000",
    "id_user": "00000000-0000-0000-0000-000000000000",
    "nb_recording_analysed": 0,
    "demo_flag": false,
    "active": true,
}
```

###### Schema
```json
{
    "id": uuid,
    "licence_type": integer,
    "serial_number": string,
    "id_order": uuid,
    "id_user": uuid,
    "nb_recording_analysed": integer,
    "demo_flag": boolean,
    "active": boolean,
}
```

##### 403 - Forbidden

##### 404 - licence-not-found

##### 404 - order-not-found

##### 403 - you-do-not-own-this-order

#### Description
> Remove a licence from an user.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return licence
> - LOCAL_ADMIN: 200 and return licence

---

## Orders

### Get orders

#### Request
```http
GET /orders
```

#### Body parameters
- state_flag : integer (optional)

#### Response

##### 200 - OK
```json
[
    {
        "id": "00000000-0000-0000-0000-000000000000",
        "order_id": "00000000-0000-0000-0000-000000000000",
        "local_admin_id": "00000000-0000-0000-0000-000000000000",
        "nb_shared_tokens": 0,
        "billing_type": 0,
        "country": "FR",
        "workplace": "Paris",
        "service": "Cardiologie",
        "seller_id": "00000000-0000-0000-0000-000000000000",
        "state_flag": 0,
        "sending_date": "1599659839",
        "order_accepted_date": "1599659839",
        "demo_flag": false,
        "sharing_authorization": false,
        "company_only": false,
    }
]
```

###### Schema
```json
[
    {
        "id": uuid,
        "order_id": uuid,
        "local_admin_id": uuid,
        "nb_shared_tokens": integer,
        "billing_type": integer,
        "country": string,
        "workplace": string,
        "service": string,
        "seller_id": uuid,
        "state_flag": integer,
        "sending_date": integer,
        "order_accepted_date": integer,
        "demo_flag": boolean,
        "sharing_authorization": boolean,
        "company_only": boolean,
    }
]
```

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Return all orders.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return all orders

---

### Get order

#### Request
```http
GET /orders/{id_order}
```

##### Path parameters
- id_order : uuid

#### Response

##### 200 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "local_admin_id": "00000000-0000-0000-0000-000000000000",
    "nb_shared_tokens": 0,
    "billing_type": 0,
    "country": "FR",
    "workplace": "Paris",
    "service": "Cardiologie",
    "seller_id": "00000000-0000-0000-0000-000000000000",
    "state_flag": 0,
    "sending_date": "1599659839",
    "oder_accepted_date": "1599659839",
    "demo_flag": false,
    "sharing_authorization": false,
    "company_only": false,
}
```

###### Schema
```json
{
    "id": uuid,
    "order_id": uuid,
    "local_admin_id": uuid,
    "nb_shared_tokens": integer,
    "billing_type": integer,
    "country": string,
    "workplace": string,
    "service": string,
    "seller_id": uuid,
    "state_flag": integer,
    "sending_date": integer,
    "order_accepted_date": integer,
    "demo_flag": boolean,
    "sharing_authorization": boolean,
    "company_only": boolean,
}
```

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Return an order's informations.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return order's informations

---

### Get order users

#### Request
```http
GET /orders/{id_order}/users
```

##### Path parameters
- id_order : uuid

#### Response

##### 200 - OK
```json
[
    {
        "type_2fa": 0,
        "licence_type": 0,
        "email": "john.doe@test.com",
        "firstname": "John",
        "lastname": "Doe",
    }
]
```

###### Schema
```json
[
    {
        "type_2fa": integer,
        "licence_type": integer,
        "email": string,
        "firstname": string,
        "lastname": string,
    }
]
```

##### 403 - Forbidden

##### 404 - order-not-found

##### 404 - user-not-found

#### Description
> Return all users linked to an order.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return all users linked to an order
> - LOCAL_ADMIN: 200 and return all users linked to an order

---

### Get order informations

#### Request
```http
GET /orders/{id_order}/about
```

##### Path parameters
- id_order : uuid

#### Response

##### 200 - OK
```json
{
    "local_admin": {
        "email": "local_admin@test.com",
        "firstname": "local_admin_firstname",
        "lastname": "local_admin_lastname",
    },
    "users": [
        {
            "type_2fa": 0,
            "licence_type": 0,
            "id_licence": "00000000-0000-0000-0000-000000000000",
            "email": "john.doe@test.com",
            "firstname": "John",
            "lastname": "Doe",
        },
    ],
    "seller": {
        "email": "seller@test.com",
        "firstname": "seller_firstname",
        "lastname": "seller_lastname",
        "phone": "0123456789",
    },
    "sum_of_recording_analysed_in_order": 0,
}
```

###### Schema
```json
{
    "local_admin": {
        "email": string,
        "firstname": string,
        "lastname": string,
    },
    "users": [
        {
            "type_2fa": integer,
            "licence_type": integer,
            "id_licence": uuid,
            "email": string,
            "firstname": string,
            "lastname": string,
        },
    ],
    "seller": {
        "email": string,
        "firstname": string,
        "lastname": string,
        "phone": string,
    },
    "sum_of_recording_analysed_in_order": integer,
}
```

##### 403 - Forbidden

##### 404 - order-not-found

##### 404 - user-not-found

#### Description
> Return all informations about an order (local admin, users, seller, sum of recording analysed in order).
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return all informations about an order

---

### Get order attachement

#### Request
```http
GET /orders/{id_order}/attachement
```

##### Path parameters
- id_order : uuid

#### Response

##### 200 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "filename": "order.xlsx",
    "created": 0,
    "size": 0,
    "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}
```

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Return an order's attachement.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return order's attachement

---

### Post order

#### Request
```http
POST /orders
```

#### Body
```json
{
    "demo_flag": false,
    "company_only": false,
    "sharing_authorization": false,
    "order_id": "00000000-0000-0000-0000-000000000000",
    "local_admin_email": "local_admin@test.com",
    "local_admin_firstname": "local_admin_firstname",
    "local_admin_lastname": "local_admin_lastname",
    "billing_type": 0,
    "country": "FR",
    "workplace": "Paris",
    "service": "Cardiologie",
    "users": [
        {
            "email": "john.doe@test.com",
            "type_2fa": 0,
            "licence_type": 0,
            "firstname": "John",
            "lastname": "Doe",
        }
    ],
    "seller_email": "seller@test.com",
    "seller_firstname": "seller_firstname",
    "seller_lastname": "seller_lastname",
    "seller_phone": "0123456789",
}
```

###### Schema
```json
{
    "demo_flag": boolean,
    "company_only": boolean,
    "sharing_authorization": boolean,
    "order_id": uuid,
    "local_admin_email": string,
    "local_admin_firstname": string,
    "local_admin_lastname": string,
    "billing_type": integer,
    "country": string,
    "workplace": string,
    "service": string,
    "users": [
        {
            "email": string,
            "type_2fa": integer,
            "licence_type": integer,
            "firstname": string,
            "lastname": string,
        }
    ],
    "seller_email": string,
    "seller_firstname": string,
    "seller_lastname": string,
    "seller_phone": string || null,
}
```

#### Response

##### 201 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "local_admin_id": "00000000-0000-0000-0000-000000000000",
    "nb_shared_tokens": 0,
    "billing_type": 0,
    "country": "FR",
    "workplace": "Paris",
    "service": "Cardiologie",
    "seller_id": "00000000-0000-0000-0000-000000000000",
    "state_flag": 0,
    "sending_date": "1599659839",
    "order_accepted_date": "1599659839",
    "demo_flag": false,
    "sharing_authorization": false,
    "company_only": false,
}
```

###### Schema
```json
{
    "id": uuid,
    "order_id": uuid,
    "local_admin_id": uuid,
    "nb_shared_tokens": integer,
    "billing_type": integer,
    "country": string,
    "workplace": string,
    "service": string,
    "seller_id": uuid,
    "state_flag": integer,
    "sending_date": integer,
    "order_accepted_date": integer,
    "demo_flag": boolean,
    "sharing_authorization": boolean,
    "company_only": boolean,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 500 - error-while-generating-serial-number

##### 400 - user-licence-type-error

#### Description
> Create a new order.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 201 and return order's informations

---

### Post order attachement

#### Request
```http
POST /orders/{id_order}/attachement
```

##### Path parameters
- id_order : uuid

#### Body
```json
{
    "file": "base64"
}
```

###### Schema
```json
{
    "file": string
}
```

#### Response

##### 201 - OK
```json
{
    "message": "File uploaded successfully",
}
```

###### Schema
```json
{
    "message": string
}
```

##### 403 - Forbidden

##### 400 - Bad Request

##### 404 - order-not-found

##### 500 - error-while-uploading-file

#### Description
> Upload an order's attachement.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return message

---

### Patch order

#### Request
```http
PATCH /orders/{id_order}
```

##### Path parameters
- id_order : uuid

#### Body
```json
{
    "order_id": "00000000-0000-0000-0000-000000000000",
    "workplace": "Paris",
    "service": "Cardiologie",
    "seller_id": "00000000-0000-0000-0000-000000000000",
    "state_flag": 0,
}
```

###### Schema
```json
{
    "order_id": uuid,
    "workplace": string,
    "service": string,
    "seller_id": uuid,
    "state_flag": integer,
}
```

#### Response

##### 204 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "local_admin_id": "00000000-0000-0000-0000-000000000000",
    "nb_shared_tokens": 0,
    "billing_type": 0,
    "country": "FR",
    "workplace": "Paris",
    "service": "Cardiologie",
    "seller_id": "00000000-0000-0000-0000-000000000000",
    "state_flag": 0,
    "sending_date": "1599659839",
    "order_accepted_date": "1599659839",
    "demo_flag": false,
    "sharing_authorization": false,
    "company_only": false,
}
```

###### Schema
```json
{
    "id": uuid,
    "order_id": uuid,
    "local_admin_id": uuid,
    "nb_shared_tokens": integer,
    "billing_type": integer,
    "country": string,
    "workplace": string,
    "service": string,
    "seller_id": uuid,
    "state_flag": integer,
    "sending_date": integer,
    "order_accepted_date": integer,
    "demo_flag": boolean,
    "sharing_authorization": boolean,
    "company_only": boolean,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Update an order's.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return order's informations

---

### Patch order billing type

#### Request
```http
PATCH /orders/type/{id_order}
```

##### Path parameters
- id_order : uuid

#### Body
```json
{
    "billing_type": 0,
}
```

###### Schema
```json
{
    "billing_type": integer,
}
```

#### Response

##### 204 - OK
```json
{
    "status_code": "204",
    "message": "Order billing type updated",
}
```

###### Schema
```json
{
    "status_code": string,
    "message": string,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Update an order's billing type.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 204 and return message

---

### Patch order sharing authorization

#### Request
```http
PATCH /orders/sharing_authorization/{id_order}
```

##### Path parameters
- id_order : uuid

#### Body
```json
{
    "sharing_authorization": false,
}
```

###### Schema
```json
{
    "sharing_authorization": boolean,
}
```

#### Response

##### 204 - OK
```json
{
    "status_code": "204",
    "message": "Order sharing authorization updated",
}
```

###### Schema
```json
{
    "status_code": string,
    "message": string,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Update an order's sharing authorization.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 204 and return message

---

### Delete order

#### Request
```http
DELETE /orders/{id_order}
```

##### Path parameters
- id_order : uuid

#### Response

##### 204 - OK
```json
{
    "message": "Order deleted",
}
```

###### Schema
```json
{
    "message": string,
}
```

##### 403 - Forbidden

##### 404 - order-not-found

#### Description
> Delete an order and all users linked to it.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 204 and return message

---

## Sellers

### Get sellers

#### Request
```http
GET /sellers
```

#### Response

##### 200 - OK
```json
[
    {
        "id": "00000000-0000-0000-0000-000000000000",
        "email": "seller@test.com",
        "firstname": "seller_firstname",
        "lastname": "seller_lastname",
        "phone": "0123456789",
    }
]
```

###### Schema
```json
[
    {
        "id": uuid,
        "email": string,
        "firstname": string,
        "lastname": string,
        "phone": string,
    }
]
```

##### 403 - Forbidden

#### Description
> Return all sellers.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return all sellers

---

### Get seller

#### Request
```http
GET /sellers/{id_seller}
```

##### Path parameters
- id_seller : uuid

#### Response

##### 200 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "email": "seller@test.com",
    "firstname": "seller_firstname",
    "lastname": "seller_lastname",
    "phone": "0123456789",
}
```

###### Schema
```json
{
    "id": uuid,
    "email": string,
    "firstname": string,
    "lastname": string,
    "phone": string || null,
}
```

##### 403 - Forbidden

##### 404 - seller-not-found

#### Description
> Return a seller.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return seller

---

## Tickets

### Get tickets

#### Request
```http
GET /tickets
```

#### Body parameters
- id_user : uuid (optional)
- state_flag : integer (optional)

#### Response

##### 200 - OK
```json
[
    {
        "id": "00000000-0000-0000-0000-000000000000",
        "id_order": "00000000-0000-0000-0000-000000000000",
        "order_id": "00000000-0000-0000-0000-000000000000",
        "workplace": "Paris",
        "service": "Cardiologie",
        "user": "00000000-0000-0000-0000-000000000000",
        "type": 0,
        "sending_date": "1599659839",
        "body": {
            "id": null,
            "type_2fa": 0,
            "email": "john.doe@test.com",
            "new_email": "john.doe@test.com",
            "firstname": "John",
            "lastname": "Doe",
            "serial_number": null,
            "licence_type": null,
        },
        "state_flag": 0,
        "update_state_date": null,
    }
]
```

###### Schema
```json
[
    {
        "id": uuid,
        "id_order": uuid,
        "order_id": uuid,
        "workplace": string,
        "service": string,
        "user": uuid,
        "type": integer,
        "sending_date": integer,
        "body": {
            "id": uuid || null,
            "type_2fa": integer,
            "email": string,
            "new_email": string || null,
            "firstname": string,
            "lastname": string,
            "serial_number": string || null,
            "licence_type": integer || null,
        },
        "state_flag": integer,
        "update_state_date": integer || null,
    }
]
```

##### 403 - Forbidden

#### Description
> Return all tickets.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return all tickets
> - LOCAL_ADMIN: 200 and return local admin's tickets

---

### Get ticket

#### Request
```http
GET /tickets/{id_ticket}
```

##### Path parameters
- id_ticket : uuid

#### Response

##### 200 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "id_order": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "workplace": "Paris",
    "service": "Cardiologie",
    "user": "00000000-0000-0000-0000-000000000000",
    "type": 0,
    "sending_date": "1599659839",
    "body": {
        "id": null,
        "type_2fa": 0,
        "email": "john.doe@test.com",
        "new_email": "john.doe@test.com",
        "firstname": "John",
        "lastname": "Doe",
        "serial_number": null,
        "licence_type": null,
    },
    "state_flag": 0,
    "update_state_date": null,
}
```

###### Schema
```json
{
    "id": uuid,
    "id_order": uuid,
    "order_id": uuid,
    "workplace": string,
    "service": string,
    "user": uuid,
    "type": integer,
    "sending_date": integer,
    "body": {
        "id": uuid || null,
        "type_2fa": integer,
        "email": string,
        "new_email": string || null,
        "firstname": string,
        "lastname": string,
        "serial_number": string || null,
        "licence_type": integer || null,
    },
    "state_flag": integer,
    "update_state_date": integer || null,
}
```

##### 403 - Forbidden

##### 404 - ticket-not-found

##### 403 - you-do-not-own-this-ticket

#### Description
> Return a ticket's informations.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return ticket's informations
> - LOCAL_ADMIN: 200 and return ticket's informations

---

### Post ticket

#### Request
```http
POST /tickets
```

#### Body
```json
{
    "id_order": "00000000-0000-0000-0000-000000000000",
    "type": 0,
    "body": {
        "type_2fa": 0,
        "licence_type": 0,
        "serial_number": "YB2307900E",
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@test.com",
    }
}
```

###### Schema
```json
{
    "id_order": uuid,
    "type": integer,
    "body": {
        "type_2fa": integer,
        "licence_type": integer,
        "serial_number": string || null,
        "firstname": string,
        "lastname": string,
        "email": string,
    }
}
```

#### Response

##### 201 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "id_order": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "workplace": "Paris",
    "service": "Cardiologie",
    "user": "00000000-0000-0000-0000-000000000000",
    "type": 0,
    "sending_date": "1599659839",
    "body": {
        "id": "00000000-0000-0000-0000-000000000000",
        "type_2fa": 0,
        "email": "john.doe@test.com",
        "new_email": "john.doe@test.com",
        "firstname": "John",
        "lastname": "Doe",
        "serial_number": "YB2307900E",
        "licence_type": 0,
    },
    "state_flag": 0,
    "update_state_date": null,
}
```

###### Schema
```json
{
    "id": uuid,
    "id_order": uuid,
    "order_id": uuid,
    "workplace": string,
    "service": string,
    "user": uuid,
    "type": integer,
    "sending_date": integer,
    "body": {
        "id": uuid || null,
        "type_2fa": integer,
        "email": string,
        "new_email": string || null,
        "firstname": string,
        "lastname": string,
        "serial_number": string || null,
        "licence_type": integer || null,
    },
    "state_flag": integer,
    "update_state_date": integer || null,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - order-not-found

##### 403 - you-do-not-own-this-order

##### 403 - licence-not-available

##### 404 - user-not-found

#### Description
> Create a new ticket.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return ticket's informations
> - LOCAL_ADMIN: 200 and return ticket's informations

---

### Patch ticket

#### Request
```http
PATCH /tickets/{id_ticket}
```

##### Path parameters
- id_ticket : uuid

#### Body
```json
{
    "type": 0,
    "body" : {
        "id": "00000000-0000-0000-0000-000000000000",
        "type_2fa": 0,
        "email": "john.doe@test.com",
        "new_email": "john.doe@test.com",
        "firstname": "John",
        "lastname": "Doe",
        "serial_number": "YB2307900E",
        "licence_type": 0,
    },
    "state_flag": 0,
}
```

###### Schema
```json
{
    "type": integer,
    "body" : {
        "id": uuid || null,
        "type_2fa": integer,
        "email": string,
        "new_email": string || null,
        "firstname": string,
        "lastname": string,
        "serial_number": string || null,
        "licence_type": integer || null,
    },
    "state_flag": integer,
}
```

#### Response

##### 204 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "id_order": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "workplace": "Paris",
    "service": "Cardiologie",
    "user": "00000000-0000-0000-0000-000000000000",
    "type": 0,
    "sending_date": "1599659839",
    "body": {
        "id": "00000000-0000-0000-0000-000000000000",
        "type_2fa": 0,
        "email": "john.doe@test.com",
        "new_email": "john.doe@test.com",
        "firstname": "John",
        "lastname": "Doe",
        "serial_number": "YB2307900E",
        "licence_type": 0,
    },
    "state_flag": 0,
    "update_state_date": null,
}
```

###### Schema
```json
{
    "id": uuid,
    "id_order": uuid,
    "order_id": uuid,
    "workplace": string,
    "service": string,
    "user": uuid,
    "type": integer,
    "sending_date": integer,
    "body": {
        "id": uuid || null,
        "type_2fa": integer,
        "email": string,
        "new_email": string || null,
        "firstname": string,
        "lastname": string,
        "serial_number": string || null,
        "licence_type": integer || null,
    },
    "state_flag": integer,
    "update_state_date": integer || null,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - ticket-not-found

##### 403 - you-do-not-own-this-ticket

##### 403 - ticket-already-closed

#### Description
> Update a ticket's informations.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return ticket's informations
> - LOCAL_ADMIN: 200 and return ticket's informations

---

### Patch process ticket

#### Request
```http
PATCH /tickets/{id_ticket}/process
```

##### Path parameters
- id_ticket : uuid

#### Body
```json
{
    "state_flag": 2,
    "body": null,
}
```

###### Schema
```json
{
    "state_flag": integer,
    "body": string || null (only when ticket is denied -> state_flag == 3)
}
```

#### Response

##### 204 - OK
```json
{
    "id": "00000000-0000-0000-0000-000000000000",
    "id_order": "00000000-0000-0000-0000-000000000000",
    "order_id": "00000000-0000-0000-0000-000000000000",
    "workplace": "Paris",
    "service": "Cardiologie",
    "user": "00000000-0000-0000-0000-000000000000",
    "type": 0,
    "sending_date": "1599659839",
    "body": {
        "id": "00000000-0000-0000-0000-000000000000",
        "type_2fa": 0,
        "email": "john.doe@test.com",
        "new_email": "john.doe@test.com",
        "firstname": "John",
        "lastname": "Doe",
        "serial_number": "YB2307900E",
        "licence_type": 0,
    },
    "state_flag": 2,
    "update_state_date": "1599659839",
}
```

###### Schema
```json
{
    "id": uuid,
    "id_order": uuid,
    "order_id": uuid,
    "workplace": string,
    "service": string,
    "user": uuid,
    "type": integer,
    "sending_date": integer,
    "body": {
        "id": uuid || null,
        "type_2fa": integer,
        "email": string,
        "new_email": string || null,
        "firstname": string,
        "lastname": string,
        "serial_number": string || null,
        "licence_type": integer || null,
    },
    "state_flag": integer,
    "update_state_date": integer || null,
}
```

##### 422 - Unprocessable Entity

##### 403 - Forbidden

##### 404 - ticket-not-found

##### 404 - order-not-found

##### 404 - licence-not-found

##### 404 - user-not-found

#### Description
> Process a ticket and create a new user or modify one if ticket is accepted.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>
> ---
> - HDS_ADMIN_MICROPORT: 200 and return ticket's informations

---

### Delete ticket

#### Request
```http
DELETE /tickets/{id_ticket}
```

##### Path parameters
- id_ticket : uuid

#### Response

##### 204 - OK
```json
{
    "message": "Ticket deleted",
}
```

###### Schema
```json
{
    "message": string,
}
```

##### 403 - Forbidden

##### 404 - ticket-not-found

##### 403 - you-do-not-own-this-ticket

##### 403 - ticket-already-closed

#### Description
> Delete a ticket.
>
> ---
> Who can access it:
>   - HDS_ADMIN_MICROPORT
>   - LOCAL_ADMIN
>
> ---
> - HDS_ADMIN_MICROPORT: 204 and return message
> - LOCAL_ADMIN: 204 and return message

---
-->