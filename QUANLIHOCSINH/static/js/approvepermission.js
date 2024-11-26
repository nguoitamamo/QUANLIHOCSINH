function DuyetPermissionUser(permissionvalue, username) {
    fetch('/approvepermission', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            permissionvalue: permissionvalue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert("Người dùng đã có quyền này");
            window.location.reload();
        }
    })
}


function ActiveAccount(username) {
    fetch('/acctiveaccount', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
}
