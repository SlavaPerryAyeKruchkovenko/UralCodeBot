import React from 'react';
import {Flex} from "antd";
import {ReactECharts} from "../../components/ReactECharts";

const Main = () => {
    return (
        <div style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
        }}>
            <ReactECharts style={{width: '600px', height: '350px'}} option={{
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                legend: {
                    bottom: 0,
                    data: ['Без каски', 'Открыл дверь', 'Вошел, когда робот работает']
                },
                toolbox: {
                    show: true,
                    orient: 'vertical',
                    left: 'right',
                    top: 'center',
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar', 'stack']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                xAxis: [
                    {
                        type: 'category',
                        axisTick: {show: false},
                        data: ['ИЮН', 'ИЮЛ', 'АВГ', 'СЕНТ']
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'Без каски',
                        type: 'bar',
                        barGap: 0,
                        emphasis: {
                            focus: 'series'
                        },
                        data: [320, 332, 301, 334, 390]
                    },
                    {
                        name: 'Открыл дверь',
                        type: 'bar',
                        emphasis: {
                            focus: 'series'
                        },
                        data: [220, 182, 191, 234, 290]
                    },
                    {
                        name: 'Вошел, когда робот работает',
                        type: 'bar',
                        emphasis: {
                            focus: 'series'
                        },
                        data: [150, 232, 201, 154, 190]
                    },
                ]
            }}/>

            <div style={{marginLeft: '30px'}}>
                <ReactECharts style={{width: '350px', height: '300px'}} option={
                    {
                        tooltip: {
                            trigger: 'item'
                        },
                        legend: {
                            bottom: '0',
                            left: 'center'
                        },
                        grid: {
                            width: '100%',
                            height: '100%'
                        },
                        series: [
                            {
                                name: 'Нарушений с роботом',
                                type: 'pie',
                                radius: ['35%', '67%'],
                                avoidLabelOverlap: false,
                                itemStyle: {
                                    borderRadius: 10,
                                    borderColor: '#fff',
                                    borderWidth: 2
                                },
                                label: {
                                    show: false,
                                    position: 'center'
                                },
                                emphasis: {
                                    label: {
                                        show: true,
                                        fontSize: 40,
                                        fontWeight: 'bold'
                                    }
                                },
                                labelLine: {
                                    show: false
                                },
                                data: [
                                    {value: 1048, name: 'Робот №3'},
                                    {value: 735, name: 'Робот №6'},
                                    {value: 580, name: 'Робот №1'},
                                    {value: 484, name: 'Робот №32'},
                                    {value: 300, name: 'Робот №12'}
                                ]
                            }
                        ]
                    }
                }/>
            </div>

        </div>
    );
};

export default Main;