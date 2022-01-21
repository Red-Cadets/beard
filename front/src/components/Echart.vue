<template>
  <div>
    <h1 style="font-family: 'Play', sans-serif;">Текущий раунд: {{ CurRound }}</h1>
    <h1 style="font-family: 'Play', sans-serif;">Времени до чека: {{ Tick }}</h1>
    <details open>
      <summary>Scores</summary>
      <v-chart v-if="this.config.EXTEND_ROUND" class='chart' :option='options' autoresize/>
    </details>
    <details open>
      <summary>Flags lost</summary>
      <v-chart class='chart' :option='flagsLost' autoresize/>
    </details>
    <details open>
      <summary>Flags got</summary>
      <v-chart class='chart' :option='flagsGot' autoresize/>
    </details>
  </div>
</template>

<script>
// TODO: рефакторинг жесткий
import { use } from 'echarts/core'

import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, HeatmapChart } from 'echarts/charts'
import {
  MarkAreaComponent,
  ToolboxComponent,
  GridComponent,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  VisualMapComponent
} from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
import moment from 'moment'

use([
  MarkAreaComponent,
  GridComponent,
  ToolboxComponent,
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  VisualMapComponent,
  HeatmapChart
])

export default {
  name: 'echart',
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: 'westeros'
  },
  props: ['quantity'],
  data () {
    return {
      rounds: [],
      teams: new Set(),
      teamsSeries: [],
      services: new Set(),

      flagsPlus: [],
      flagsMinus: [],
      roundsN: [],

      config: {},

      maxScore: 0,
      teamScore: 0,
      maxLost: 0,
      maxGot: 0,

      curRound: 0,
      curRoundTime: 0,
      firstRound: 0,
      firstRoundTime: 0,

      time: 0
    }
  },
  computed: {
    flagsGot () {
      return {
        tooltip: {
          position: 'top'
        },
        grid: {
          left: '1%',
          right: '5%',
          top: '13%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: this.roundsN,
          splitArea: {
            show: true
          },
          scrollbar: {
            enabled: true
          }
        },
        yAxis: {
          type: 'category',
          data: Array.from(this.services),
          splitArea: {
            show: true
          }
        },
        dataZoom: [
          {
            start: this.startZoomRound,
            end: 100,
            realTime: true
          }
        ],
        visualMap: {
          min: 0,
          max: this.maxGot,
          calculable: true,
          inRange: {
            color: [ '#7AFB95', '#0B7621' ] // Зелёный
          },
          orient: 'vertical',
          right: '0%',
          bottom: '30%'
        },
        series: [
          {
            name: 'Получено флагов',
            type: 'heatmap',
            data: this.flagsPlus.map(function (item) { return [item[1], item[0], item[2] || '-'] }),
            label: {
              show: true
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    },
    flagsLost () {
      return {
        tooltip: {
          position: 'top'
        },
        grid: {
          left: '1%',
          right: '5%',
          top: '13%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: this.roundsN,

          scrollbar: {
            enabled: true
          }
        },
        yAxis: {
          type: 'category',
          data: Array.from(this.services)
        },
        dataZoom: [
          {
            start: this.startZoomRound,
            end: 100,
            realTime: true
          }
        ],
        visualMap: {
          min: 0,
          max: this.maxLost,
          calculable: true,
          inRange: {
            color: [ '#F2A1A1', '#CB0000' ] // Красный
          },
          orient: 'vertical',
          right: '0%',
          bottom: '30%'
        },
        series: [
          {
            name: 'Утеряно флагов',
            type: 'heatmap',
            data: this.flagsMinus.map(function (item) { return [item[1], item[0], item[2] || '-'] }),
            label: {
              show: true
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    },
    startZoomTime () {
      if (this.curRound < this.config.EXTEND_ROUND * 3) {
        return 0
      }
      return (this.curRoundTime.unix() - this.firstRoundTime.unix() - this.config.ROUND_TIME * this.config.EXTEND_ROUND * 3) / (this.curRoundTime.unix() - this.firstRoundTime.unix() + this.config.ROUND_TIME * this.config.EXTEND_ROUND) * 100
    },
    endZoomScore () {
      return this.teamScore * 150 / this.maxScore
    },
    startZoomRound () {
      if (this.curRound < this.config.EXTEND_ROUND * 3) {
        return 0
      }
      return (this.curRound - this.firstRound - this.config.EXTEND_ROUND * 3) / (this.curRound - this.firstRound + this.config.EXTEND_ROUND) * 100
    },
    CurRound () {
      return this.curRound
    },
    Tick () {
      return this.time
    },
    options () {
      return {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          type: 'scroll',
          right: 10,
          top: 25,
          bottom: 20,
          data: Array.from(this.teams)
        },
        grid: {
          left: '1%',
          right: '5%',
          top: '13%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'time',
          boundaryGap: false,
          name: 'Round',
          axisLabel: {
            rotate: 30,
            formatter: function (value) {
              return moment(value).format('Do, HH:mm')
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'Score'
        },
        dataZoom: [
          {
            start: this.startZoomTime,
            xAxisIndex: 0,
            end: 100
          },
          {
            start: 0,
            yAxisIndex: 0,
            end: this.endZoomScore
          }
        ],
        series: this.teamsSeries
      }
    }
  },
  methods: {
    getInfo: function () {
      // ? Получаем информацию из бд
      this.axios.get(`http://${window.location.hostname}:8888/api/info`)
        .then(result => {
          result = result.data
          var teamsInfo = {}
          var info = []
          if (result.length > 0) {
            this.firstRound = result[0]['round']
            this.firstRoundTime = moment(result[0]['time'], 'YYYY-MM-DD HH:mm:ss')
            // ? Сохраняем названия команд
            for (var res of result[0]['teams_info']) {
              var teamName = res['name']
              this.teams.add(teamName)
              teamsInfo[teamName] = {
                'name': teamName,
                'showSymbol': false,
                'type': 'line',
                emphasis: {
                  focus: 'series'
                },
                smooth: true,
                data: []
              }
              if (teamName === this.config.TEAM) {
                teamsInfo[teamName]['lineStyle'] = {
                  normal: {
                    width: 4
                  }
                }
              }
            }
            // ? Преобразовываем информацию из бд
            for (var i = 0; i < result.length; i++) {
              var curTime = moment(result[i]['time'], 'YYYY-MM-DD HH:mm:ss')
              this.curRoundTime = curTime
              this.rounds.push(result[i]['time'])
              var infos = result[i]['teams_info']
              for (info of infos) {
                teamName = info['name']
                if (teamName === this.config.TEAM) {
                  this.teamScore = info['score']
                }
                teamsInfo[teamName]['data'].push([result[i]['time'], info['score']])
              }
            }
            this.teamsSeries = []
            this.curRound = result[result.length - 1]['round']

            // ? Extend
            curTime.add(this.config.ROUND_TIME * this.config.EXTEND_ROUND, 'seconds')
            this.rounds.push(curTime.format('YYYY-MM-DD HH:mm:ss'))
            var growth = 0
            for (info of Object.values(teamsInfo)) {
              var data = info['data']
              var dataLen = data.length
              if (dataLen > 4) {
                growth = ((data[dataLen - 1][1] - data[dataLen - 2][1]) +
                          (data[dataLen - 2][1] - data[dataLen - 3][1]) +
                          (data[dataLen - 3][1] - data[dataLen - 4][1]) +
                          (data[dataLen - 4][1] - data[dataLen - 5][1])) / 4
              } else {
                growth = 0
              }
              var lastData = data[dataLen - 1]
              var growedData = lastData[1] + growth * this.config.EXTEND_ROUND
              info['data'].push([curTime.format('YYYY-MM-DD HH:mm:ss'), growedData])
              this.maxScore = this.maxScore < growedData * 1.1 ? growedData * 1.1 : this.maxScore
              this.teamsSeries.push(info)
            }
            // ? Вертикальная линяя текущего раунда
            // TODO Переписать костыль
            // ХЗ ПОЧЕМУ СЛЕДУЮЩИЙ КОД У ВАС НЕ РОБИТ)
            /*
              markLine: {
                silent: true,
                symbol: [],
                label: {
                  show: false,
                },
                lineStyle: {
                  color: '#333'
                },
                data: [
                  {
                    xAxis: result[result.length - 1]['time']
                  },
                ]
              }
            */
            var vertData = []
            for (i = 0; i < this.maxScore; i += this.maxScore / 100) {
              vertData.push([result[result.length - 1]['time'], i])
            }
            this.teamsSeries.push({
              'name': 'Текущий раунд',
              'showSymbol': false,
              'type': 'line',
              emphasis: { focus: 'series' },
              lineStyle: { type: 'dashed' },
              smooth: true,
              data: vertData
            })
          }
        })
      this.axios.get(`http://${window.location.hostname}:8888/api/team_info`)
        .then(result => {
          result = result.data
          if (result.length > 0) {
            for (var serviceName of Object.keys(result[0]['services'])) {
              this.services.add(serviceName)
            }
            for (var i = 0; i < result.length; i++) {
              this.roundsN.push(result[i]['round'].toString())
              for (var [j, ser] of Object.entries(Array.from(this.services))) {
                this.maxLost = this.maxLost < result[i]['services'][ser]['flags']['lost'] ? result[i]['services'][ser]['flags']['lost'] : this.maxLost
                this.maxGot = this.maxGot < result[i]['services'][ser]['flags']['got'] ? result[i]['services'][ser]['flags']['got'] : this.maxGot
                this.flagsPlus.push([parseInt(j), result[i]['round'].toString(), result[i]['services'][ser]['flags']['got']])
                this.flagsMinus.push([parseInt(j), result[i]['round'].toString(), result[i]['services'][ser]['flags']['lost']])
              }
            }
          }
        })
    },
    storeConfig: function () {
      this.axios.get(`http://${window.location.hostname}:8888/api/config`)
        .then(result => {
          this.config = result.data
        })
    },
    updateInfo: function (data) {
      var info = data['info']
      var curTime = moment(info['time'], 'YYYY-MM-DD HH:mm:ss')
      this.curRoundTime = curTime
      this.rounds.pop()
      this.rounds.push(info['time'])
      // ? Extend
      curTime.add(this.config.ROUND_TIME * this.config.EXTEND_ROUND, 'seconds')
      this.rounds.push(curTime.format('YYYY-MM-DD HH:mm:ss'))
      var growth = 0

      this.curRound = info['round']
      var infos = info['teams_info']
      for (var Info of infos) {
        var teamName = Info['name']
        if (teamName === this.config.TEAM) {
          this.teamScore = Info['score']
        }
        for (var teamSeries of this.teamsSeries) {
          if (teamSeries['name'] === teamName) {
            teamSeries['data'].pop()
            teamSeries['data'].push([info['time'], Info['score']])
            var d = teamSeries['data']
            var dataLen = d.length
            if (dataLen > 4) {
              growth = ((d[dataLen - 1][1] - d[dataLen - 2][1]) +
                        (d[dataLen - 2][1] - d[dataLen - 3][1]) +
                        (d[dataLen - 3][1] - d[dataLen - 4][1]) +
                        (d[dataLen - 4][1] - d[dataLen - 5][1])) / 4
            } else {
              growth = 0
            }
            var growedData = Info['score'] + growth * this.config.EXTEND_ROUND
            teamSeries['data'].push([curTime.format('YYYY-MM-DD HH:mm:ss'), growedData])
            this.maxScore = this.maxScore < growedData * 1.1 ? growedData * 1.1 : this.maxScore
          } else if (teamSeries['name'] === 'Текущий раунд') {
            teamSeries['data'] = [[info['time'], 0], [info['time'], this.maxScore]]
          }
        }
      }
      var teamInfo = data['team_info']
      var sers = teamInfo['services']
      if (this.services.length === 0) {
        for (var num of Object.keys(sers)) { this.services.add(num) }
      }
      this.roundsN.push(info['round'].toString())
      for (var [n, s] of Object.entries(Array.from(this.services))) {
        this.maxLost = this.maxLost < sers[s]['flags']['lost'] ? sers[s]['flags']['lost'] : this.maxLost
        this.maxGot = this.maxGot < sers[s]['flags']['got'] ? sers[s]['flags']['got'] : this.maxGot
        this.flagsPlus.push([parseInt(n), info['round'].toString(), sers[s]['flags']['got']])
        this.flagsMinus.push([parseInt(n), info['round'].toString(), sers[s]['flags']['lost']])
      }
    },
    tickFunction () {
      if (this.time > 0) {
        this.time -= 1
      }
    }
  },
  created () {
    this.$options.sockets.onmessage = function (evt) {
      // ? Добавляем новую информацию
      this.updateInfo(JSON.parse(evt.data))
      this.time = this.config.ROUND_TIME
    }
    this.$options.sockets.onopen = () => {
      // ? Сообщаем серверу о себе
      this.$socket.send(JSON.stringify({'type': 'connect', 'message': 'I\'m here :3'}))
      this.storeConfig()
      this.getInfo()
    }
  },
  mounted () {
    setInterval(this.tickFunction, 1000)
  }
}
</script>

<style scoped>
.chart {
  height: 600px;
}

details {
  border: 1px solid #aaa;
  border-radius: 4px;
  padding: .5em .5em 0;
  margin-bottom: .5em;
}

summary {
  font-weight: bold;
  margin: -.5em -.5em 0;
  padding: .5em;
}

details[open] {
  padding: .5em;
}

details[open] summary {
  border-bottom: 1px solid #aaa;
  margin-bottom: .5em;
}
</style>
