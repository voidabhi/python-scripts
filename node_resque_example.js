

// worker


import { queue } from '../initializers/node_resque'


function perform(id, done) {
  // i need to enqueue another worker from here
  // suppose importing queue from the initializer may be wrong
  queue.scheduledAt('test-app', 'worker2', id, (err, timestamps) => {
    if (timestamps.length > 0) {
      done(null, true)
    } else {
      queue.enqueueIn(20000, 'test-app', 'worker2', id, () => {
        console.log('enqueued worker2')
        done(null, true)
      })
    }
  })
}


export { perform }


// server

import schedule from 'node-schedule'
import NR from 'node-resque'
import Redis from 'ioredis'
import workers from '../workers'

const redisClient = new Redis(process.env.REDIS_URL)
const queue = new NR.queue({ connection: { redis: redisClient } }, workers)

const worker = new NR.multiWorker({
  connection: { redis: redisClient },
  queues: 'test-app',
  minTaskProcessors: 1,
  maxTaskProcessors: 20,
}, workers)

const scheduler = new NR.scheduler({ connection: { redis: redisClient } })


function stop() {
  scheduler.end(() => {
    worker.end(() => {
      process.exit(0)
    })
  })
}

function start() {
  scheduler.connect(() => {
    scheduler.start()
    console.log('started scheduler')

    worker.start()
    console.log('started worker')
  })

  queue.connect(() => {
    queue.cleanOldWorkers(5000, (err, data) => {
      if (Object.keys(data).length > 0) console.log('cleaned old workers')
    })

    schedule.scheduleJob('*/15 * * * *', () => {
      if (scheduler.master) {
        queue.enqueue('test-app', 'worker1', 1)
        console.log('enqueued scheduled job')
      }
    })
  })
}


process.on('SIGINT', stop)
process.on('SIGTERM', stop)


export { start, queue }

