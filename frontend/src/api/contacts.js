import request from './request'

export function getContacts(params) {
    return request({
        url: '/contacts',
        method: 'get',
        params
    })
}

export function createContact(data) {
    return request({
        url: '/contacts',
        method: 'post',
        data
    })
}

export function updateContact(id, data) {
    return request({
        url: `/contacts/${id}`,
        method: 'put',
        data
    })
}

export function deleteContact(id) {
    return request({
        url: `/contacts/${id}`,
        method: 'delete'
    })
}

export function toggleFavorite(id) {
    return request({
        url: `/contacts/${id}/favorite`,
        method: 'post'
    })
}

export function addContactMethod(id, data) {
    return request({
        url: `/contacts/${id}/methods`,
        method: 'post',
        data
    })
}

export function deleteContactMethod(contactId, methodId) {
    return request({
        url: `/contacts/${contactId}/methods/${methodId}`,
        method: 'delete'
    })
}

export function exportContacts() {
    // Use direct download link or blob handling
    return request({
        url: '/export',
        method: 'get',
        responseType: 'blob'
    })
}

export function importContacts(formData) {
    return request({
        url: '/import',
        method: 'post',
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}
