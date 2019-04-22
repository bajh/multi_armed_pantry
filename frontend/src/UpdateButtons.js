import React, { Component } from 'react'

export default class UpdateButtons extends Component {
    update(val) {
        const url = `/api/update?id=${this.props.id}&val=${val}`
        return fetch(url, {
            method: 'POST',
        }).then(() => this.props.onClick())
    }

    render() {
        const { color } = this.props
        return (
            <div>
                <button
                    onClick={() => this.update(1)}
                    style={{ marginRight: '5px', borderColor: color, color, borderStyle: 'solid' }}
                >
                    👍
                </button>
                <button
                    onClick={() => this.update(0)}
                    style={{ marginLeft: '5px', borderColor: color, color, borderStyle: 'solid' }}
                >
                    👎
                </button>
            </div>
        )
    }
}