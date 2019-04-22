import React, { Component } from 'react'
import UpdateButtons from './UpdateButtons'

export default class Restaurant extends Component {
    render() {
        const { restaurant } = this.props
        return (
            <div style={{ paddingBottom: '8px', marginBottom: '10px', border: '2px solid ' + restaurant.color }}>
                <div style={{ backgroundColor: restaurant.color, color: '#ecf0f1', padding: '10px 8px', marginBottom: '8px' }}>
                    {restaurant.name}
                </div>
                <UpdateButtons
                    id={restaurant.id}
                    color={restaurant.color}
                    onClick={this.props.onUpdate}
                />
            </div>
        )
    }
}