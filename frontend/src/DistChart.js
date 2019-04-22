import React, { Component } from 'react'
import Chart from 'chart.js'

export default class DistChart extends Component {
    chart = null

    createDatasets = () => 
        this.props.distributions.map(({ restaurant, distribution}) => {
            const pointRadius = [...Array(101)].map(() => 1)
            const pointColor = [...Array(101)]

            if (this.props.sampledProbabilities) {
                const sampledProb = Math.floor(this.props.sampledProbabilities[restaurant.id] * 100)
                pointRadius[sampledProb] = 6
                pointColor[sampledProb] = restaurant.color
            }
            return {
                label: restaurant.name,
                data: distribution,
                fill: false,
                borderColor: restaurant.color,
                pointRadius,
                pointStyle: 'rectRot',
                pointBackgroundColor: pointColor,
            }
        }
    )

    componentDidMount() {
        this.chart = new Chart(this.ref, {
            type: 'line',
            data: {
              labels: [...Array(101).keys()],
              datasets: this.createDatasets(),
            },
            options: {
                legend: {
                    display: false,
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            fontColor: '#ecf0f1',
                        },
                        gridLines: { color: '#34495e' },
                    }],
                    xAxes: [{
                        ticks: {
                            fontColor: '#ecf0f1',

                        },
                        gridLines: { color: '#34495e' },
                    }],
                },
            },
        })
        this.chart.canvas.parentNode.style.height = this.props.height
        this.chart.canvas.parentNode.style.width = this.props.width
    }

    componentDidUpdate() {
        this.chart.data.datasets = this.createDatasets()
        this.chart.update()
    }

    render() {
        return (
            <canvas
                style={{ backgroundColor: '#2c3e50 !important' }}
                ref={r => {this.ref = r}}
            />
        )
    }
}