# Permissions and access control

DSA uses Girder's access-control model. Every collection and folder has an
access list; items inherit access from the folder that contains them. This page
explains the model so you can choose the right role and predict who sees what.

For the step-by-step flow, see
[Share a collection or folder](../tutorials/share-a-collection.md).

## Users, groups, and roles

An access list entry is either a **user** or a **group**, with one role:

| Role | Girder level | Can view/download | Can edit properties and add content | Can delete and change access |
| --- | --- | --- | --- | --- |
| No access | — | No | No | No |
| **Can view** | `READ` | Yes | No | No |
| **Can edit** | `WRITE` | Yes | Yes | No |
| **Is owner** | `ADMIN` | Yes | Yes | Yes |

A site administrator can always take any action, regardless of the list.

Permissions are **additive**. If a user has **Can view** directly and **Can
edit** through a group, the effective role is **Can edit**. You cannot subtract
a permission by adding another entry; remove the direct grant or remove the user
from the group instead.

Use groups for anything shared by more than one person. Access follows group
membership, so adding a new lab member to the group grants every resource the
group can see, and removing them revokes it in one place.

## Private and public

Collections and folders are either private or public:

- **Private** — only users and groups on the access list, plus site
  administrators, can view it. This is the default for a new collection.
- **Public** — anyone can view it, including anonymous visitors who are not
  signed in.

Public grants view access only. It does not grant edit or owner access. Making a
folder public does not retroactively share annotations that already exist; see
below.

## Inheritance

- A collection contains folders; folders can contain subfolders and items.
- Folders inherit access from their parent folder, and items inherit from their
  folder. Items do not have their own access list.
- A child can be shared more broadly than its parent by adding entries to the
  child.
- When you change a folder's access list, you choose whether to apply the change
  only to that folder or to all subfolders as well. The subfolder option
  **replaces** the list on each subfolder; it does not merge.

To share one item without exposing its siblings, move or copy it into a folder
whose access list contains only the intended audience.

## Access flags

Access flags grant a specific capability without raising the role. DSA's
annotation plugin registers **Create annotations**, which lets a user add
annotations to items in a folder while keeping the folder read-only for
everything else. Flags are additive and appear beside each user or group in the
**Access control** dialog.

## Annotation access is separate

Annotations carry their own access list and public flag. They are not ordinary
items and do not simply follow the folder.

- When an annotation is created, it copies the access list and public flag of
  the item's folder. The creator also gets admin access to the annotation.
- That copy happens once. Changing the folder's access later does not update
  annotations that already exist.
- A user with write or admin access to a folder gets the same access to new
  annotations in that folder, including annotations created by other people.
- Moving an item or an annotation does not change the annotation's access list.
- Copying an item or folder copies its annotations and assigns the copies the
  destination folder's access.

The practical rule: **share the folder before collaborators create annotations
if you want everyone to see them.** If annotations already exist, use the
folder's **Annotation access control** action to replace their access lists in
bulk. That action is available to users with admin access to annotations in the
folder and can optionally include subfolders. Treat it carefully: it replaces
lists rather than merging them, and it runs without waiting for a result.

## Who can do what

| Action | Required access |
| --- | --- |
| View a collection, folder, item, or file | **Can view** on the collection or folder, or public |
| Upload or create a folder/item | **Can edit** on the destination folder |
| Edit metadata or properties | **Can edit** on the resource |
| Delete a collection or folder | **Is owner** on it, or site administrator |
| Change an access list | **Is owner** on the resource, or site administrator |
| Create an annotation | **Can edit** on the item's folder, or the **Create annotations** flag |
| Modify an annotation | **Can edit** on the annotation and either **Can edit** on the item's folder or the **Create annotations** flag |
| Change an annotation's access list | **Is owner** on the annotation |

## Related pages

- [Share a collection or folder](../tutorials/share-a-collection.md)
- [Create a collection](../tutorials/create-a-collection.md)
- [Create a folder](../tutorials/create-a-folder.md)
- [Annotation basics](annotations.md)
