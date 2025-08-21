# Admin Jobs

## Monitor and Manage Background Tasks

Admin Jobs lets administrators see and control all the background tasks running in Sigmatiq.

## What It Is

Admin Jobs is a control panel for:
- Viewing running tasks
- Monitoring job queues
- Cancelling stuck jobs
- Retrying failed tasks
- Tracking system workload

Think of it as mission control for all the behind-the-scenes work.

## Why It Matters

Job management helps:
- Keep system running smoothly
- Fix stuck processes
- Prioritize important tasks
- Monitor system health
- Troubleshoot problems

## Key Concepts

### Job Types

| Type | What It Does | Typical Duration |
|------|--------------|------------------|
| **Backtest** | Test strategy on historical data | 2-10 minutes |
| **Training** | Build machine learning model | 5-15 minutes |
| **Sweep** | Test multiple variations | 10-60 minutes |
| **Matrix Build** | Prepare training data | 1-5 minutes |
| **Signal Generation** | Create trade alerts | < 1 second |
| **Report Generation** | Create PDF/CSV reports | 1-3 minutes |

### Job States

| State | Meaning | Action Available |
|-------|---------|------------------|
| **Pending** | Waiting in queue | Cancel |
| **Running** | Currently processing | Stop |
| **Completed** | Finished successfully | View results |
| **Failed** | Error occurred | Retry or investigate |
| **Cancelled** | User stopped | Delete |
| **Stuck** | Not progressing | Force stop |

### Priority Levels

| Priority | Processing Order | Use For |
|----------|-----------------|---------|
| **Critical** | First | System tasks |
| **High** | Second | Live trading |
| **Normal** | Third | Most tasks |
| **Low** | Last | Reports, exports |

## Main Screen Tour

*Note: Admin access required*

### Jobs Queue Dashboard

#### Summary Cards

Top row statistics:
- **Total Jobs**: All jobs in system
- **Running**: Currently processing
- **Pending**: Waiting to start
- **Failed**: Need attention
- **Success Rate**: Percentage completed

#### Active Jobs Table

Currently running tasks:

| Column | Shows |
|--------|-------|
| **Job ID** | Unique identifier |
| **Type** | Backtest, training, etc |
| **User** | Who started it |
| **Started** | When began |
| **Progress** | Percentage complete |
| **ETA** | Estimated completion |
| **Actions** | Stop, view details |

#### Queue Table

Waiting jobs:

| Column | Shows |
|--------|-------|
| **Position** | Place in line |
| **Job Type** | What will run |
| **Priority** | High/Normal/Low |
| **User** | Requester |
| **Created** | When queued |
| **Actions** | Cancel, change priority |

#### Completed Jobs

Finished tasks:

| Column | Shows |
|--------|-------|
| **Job ID** | Reference number |
| **Type** | What ran |
| **Status** | Success/Failed |
| **Duration** | How long took |
| **Finished** | Completion time |
| **Actions** | View results, retry |

### Job Detail View

Click any job to see:

#### Overview Section
- Job ID and type
- Current status
- User information
- Time statistics
- Resource usage

#### Configuration Tab
- Input parameters
- Model settings
- Date ranges
- Options selected

#### Progress Tab
- Step-by-step status
- Current operation
- Logs preview
- Error messages

#### Results Tab
- Output location
- Metrics generated
- Files created
- Next steps

## Typical Workflows

### Daily Monitoring

1. **Check Summary**
   - Note failed jobs
   - Check queue length
   - Verify processing rate

2. **Review Failures**
   - Identify patterns
   - Common errors
   - User issues

3. **Clear Backlog**
   - Cancel old jobs
   - Retry important ones
   - Adjust priorities

### Handling Stuck Jobs

1. **Identify Stuck Job**
   - No progress in 10+ minutes
   - Status shows "Running"
   - User complaining

2. **Investigate**
   - Check logs
   - View configuration
   - Look for errors

3. **Take Action**
   - Try graceful stop
   - Force kill if needed
   - Notify user
   - Retry if appropriate

### Managing Load

1. **Monitor Queue**
   - Check pending count
   - Note wait times
   - Watch growth rate

2. **Prioritize**
   - Boost important jobs
   - Delay low priority
   - Cancel unnecessary

3. **Optimize**
   - Adjust concurrency
   - Add resources
   - Schedule maintenance

## Job Management Actions

### Stopping Jobs

Options available:

| Action | What Happens | When to Use |
|--------|--------------|-------------|
| **Graceful Stop** | Finish current step, then stop | Normal cancellation |
| **Force Stop** | Immediately terminate | Job is stuck |
| **Pause** | Temporarily halt | System maintenance |

### Retrying Jobs

When to retry:
- Temporary error
- Resource issue fixed
- Data now available
- User requests

How to retry:
1. Click failed job
2. Review error
3. Fix if needed
4. Click Retry button

### Bulk Operations

Select multiple jobs to:
- Cancel all
- Retry failed
- Change priority
- Export list
- Delete old

## Queue Management

### Queue Metrics

Monitor these:

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **Queue Length** | < 10 | 10-50 | > 50 |
| **Wait Time** | < 1 min | 1-5 min | > 5 min |
| **Processing Rate** | > 10/min | 5-10/min | < 5/min |
| **Failure Rate** | < 1% | 1-5% | > 5% |

### Priority Management

Adjust priorities:

**Boost Priority:**
- Premium users
- Time-sensitive
- Small quick jobs
- Retry attempts

**Lower Priority:**
- Large batches
- Non-urgent
- Resource heavy
- Free users

### Capacity Planning

Signs need more capacity:
- Queue always full
- Long wait times
- User complaints
- Timeouts increasing

## Common Job Issues

### "Job Failed"

Common causes:
- Invalid parameters
- Data not available
- Out of memory
- Timeout reached

Solutions:
1. Check error message
2. Verify configuration
3. Fix issue
4. Retry job

### "Job Stuck"

Indicators:
- No progress updates
- Running too long
- User can't cancel

Actions:
1. Check system health
2. View job logs
3. Force stop
4. Investigate cause

### "Queue Backed Up"

Reasons:
- Too many users
- Large jobs
- System slow
- Errors cascading

Fixes:
1. Cancel old jobs
2. Increase capacity
3. Limit submissions
4. Fix root cause

## Resource Management

### System Resources

Monitor usage:

| Resource | Normal | High | Action Needed |
|----------|--------|------|---------------|
| **CPU** | < 70% | 70-90% | > 90% |
| **Memory** | < 80% | 80-95% | > 95% |
| **Disk I/O** | < 60% | 60-80% | > 80% |
| **Network** | < 50% | 50-75% | > 75% |

### Job Resources

Typical consumption:

| Job Type | CPU | Memory | Duration |
|----------|-----|--------|----------|
| **Backtest** | Medium | Low | 5 min |
| **Training** | High | High | 10 min |
| **Sweep** | High | Medium | 30 min |
| **Signal** | Low | Low | 1 sec |

## Scheduling

### Maintenance Windows

Schedule during:
- Low usage times
- Market closed
- Weekends
- Holidays

### Batch Processing

Group jobs for efficiency:
- Similar types together
- Off-peak processing
- Resource optimization
- Reduced overhead

## Monitoring and Alerts

### Set Alerts For

Critical conditions:
- Queue > 100 jobs
- Failure rate > 10%
- Stuck jobs > 5
- Wait time > 10 min

### Alert Channels

Receive notifications:
- Email
- SMS
- Slack
- Dashboard banner

## Reports

### Available Reports

Job statistics:
- Daily summary
- User usage
- Failure analysis
- Performance trends
- Resource utilization

### Export Options

Download data:
- CSV spreadsheet
- JSON for analysis
- PDF reports
- API access

## Best Practices

### Do's ✓
- Monitor regularly
- Clear old jobs
- Investigate failures
- Document issues
- Plan capacity

### Don'ts ✗
- Ignore stuck jobs
- Let queue overflow
- Force stop everything
- Delete without checking
- Skip monitoring

## Troubleshooting

### System Slow

Check:
1. Queue length
2. Resource usage
3. Failed job count
4. Database performance

### Jobs Not Starting

Verify:
1. Queue not paused
2. Resources available
3. No system errors
4. Workers running

### High Failure Rate

Investigate:
1. Common error patterns
2. Recent changes
3. Data issues
4. User mistakes

## Next Steps

Regular tasks:
1. Daily queue check
2. Weekly failure review
3. Monthly capacity planning
4. Quarterly optimization
5. Document patterns

## Assumptions & Open Questions

**Assumptions:**
- Jobs are independent
- Resources are shared
- Priority system works

**Open Questions:**
- Job dependencies
- Custom priorities
- Resource reservation
- Scheduled jobs

---

## Related Reading

- [Options Health](./options-health.md)
- [Feature Flags](./feature-flags.md)
- [Users](./users.md)
- [Dashboard](./dashboard.md)
- [Troubleshooting](../help/troubleshooting.md)