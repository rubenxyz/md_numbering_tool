There are two main reasons to use key-based authentication:

1.  When calling [ready-to-use models](https://fal.ai/models)
2.  In headless remote environments or CI/CD (where GitHub authentication is not available)

### Generating the keys

Navigate to our dashboard keys page and generate a key from the UI [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)

### Scopes

Scopes provide a way to control the permissions and access level of a given key. By assigning scopes to keys, you can limit the operations that each key can perform. Currently there are only two scopes, `ADMIN` and `API`. If you are just consuming [ready-to-use models](https://fal.ai/models), we recommend that you use the `API` scope.

#### API scope

-   Grants access to ready-to-use models.

#### ADMIN scope

-   Grants full access to private models.
-   Grants full access to CLI operations.
-   Grants access to ready-to-use models.