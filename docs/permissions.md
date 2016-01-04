# Permissions
Permission levels are represented as powers of 2.

Permission checks are done via bitwise AND (the `&` operator)

```python
has_permissions = (required_permissions & user_permissions) == required_permissions
```

Permissions can be combined via a bitwise OR

```
READ_WRITE = CREATE | READ | UPDATE
CRUD = READ_WRITE | DELETE
```

## Permission Levels
Permission | Power | Numeric
:--------: | :---: | :-----------------:
None       | N/A   | 0
Create     | 1     | 2
Read       | 2     | 4
Update     | 3     | 8
Delete     | 4     | 16
Admin      | 63    | 9223372036854775807

Note:
> Admin permissions are actually `(2 << 63) - 1`, the binary equivalent is 64 1s.

> Any number or permission less than `(2 ^ 64) - 1` will evaluate to true when bitwise ANDed against it

## Resource Permissions

Resources store permissions as a hash of `selector` -> `permission`.

A user's permissions are equivalent to their permissions to the current resource combined and all of its parents combined via bitwise or.
```javascript
currentResource.concat(currentResource.parents)
    .map(GetPermissions)
    .reduce(bitwiseOr, permissions.NONE);
```

### Selectors
Selectors are formatted as `{user_type}-{provider}-{id}`, the same as a user id.

A selector, however, may be terminated early by the wild card character `*`

Valid seletors are:
* `*`
* `{user_type}-*`
* `{user_type}-{provider}-*`
* `{user_type}-{provider}-{user_id}`
