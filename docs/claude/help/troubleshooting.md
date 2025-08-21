# Troubleshooting Guide

## How to Fix Common Problems

This guide helps you solve common issues with Sigmatiq. Find your problem and follow the steps.

## Login Problems

### Can't Sign In

**Symptoms:**
- Wrong password error
- Account not found
- Page won't load

**Solutions:**
1. Check caps lock is off
2. Try password reset
3. Clear browser cookies
4. Try different browser
5. Check if site is down

### Two-Factor Authentication Issues

**Symptoms:**
- Code not working
- Not receiving code
- Lost phone

**Solutions:**
1. Check phone time is correct
2. Wait 30 seconds, try new code
3. Use backup codes
4. Contact support for reset

## Model Problems

### Model Not Creating

**Symptoms:**
- Create button not working
- Error message appears
- Stuck on loading

**Solutions:**
1. Check all fields filled
2. Try different name
3. Select different template
4. Refresh page
5. Check model limit

### Model Not Generating Signals

**Symptoms:**
- No signals appearing
- Signal count stays zero
- Model shows active but quiet

**Solutions:**

| Check | How to Fix |
|-------|------------|
| **Model active?** | Toggle switch to ON |
| **Market hours?** | Wait for market open |
| **Confidence too high?** | Lower threshold to 60% |
| **No market match?** | Different conditions needed |
| **Data feed working?** | Check Health page |

### Model Performance Poor

**Symptoms:**
- Losing money
- Not matching backtest
- Too many bad trades

**Solutions:**
1. Compare market conditions to backtest
2. Check if following signals exactly
3. Review slippage and costs
4. Consider paper trading
5. Try different model

## Backtest Issues

### Backtest Won't Start

**Symptoms:**
- Build button disabled
- Error on clicking
- Stuck at 0%

**Solutions:**
1. Check date range valid
2. Verify ticker exists
3. Reduce time period
4. Try different model
5. Check system health

### Backtest Failed

**Error Messages and Fixes:**

| Error | Solution |
|-------|----------|
| **"Insufficient data"** | Use longer date range or different ticker |
| **"Training failed"** | Simplify model or reduce indicators |
| **"Matrix build error"** | Check dates, try again |
| **"No trades generated"** | Lower confidence threshold |
| **"Timeout"** | Use shorter period, try again |

### Results Too Good/Bad

**Too Good (Suspicious):**
- Returns over 100% yearly
- No losing months
- Win rate over 80%

**Check for:**
1. Look-ahead bias
2. Unrealistic fills
3. Missing costs
4. Data errors

**Too Bad:**
- All losses
- Huge drawdowns
- No trades

**Try:**
1. Different time period
2. Adjust parameters
3. New template
4. Check logic

## Signal Problems

### No Signals Showing

**Symptoms:**
- Signals page empty
- Count shows zero
- Models active but no signals

**Solutions:**
1. Verify models are active
2. Check market is open
3. Lower confidence thresholds
4. Review model logic
5. Check data feed status

### Too Many Signals

**Symptoms:**
- Overwhelming alerts
- Can't keep up
- Conflicting signals

**Solutions:**
1. Raise confidence threshold
2. Reduce active models
3. Add filters
4. Focus on one pack
5. Use position limits

### Signals Not Executing

**With Broker Connected:**
- Check account balance
- Verify permissions
- Test connection
- Check order types supported
- Review broker messages

## Platform Performance

### Site Running Slow

**Symptoms:**
- Pages load slowly
- Clicks delayed
- Charts lag

**Quick Fixes:**
1. Clear browser cache
2. Close other tabs
3. Restart browser
4. Check internet speed
5. Try different browser

**Browser Cache Clear:**
- Chrome: Settings → Privacy → Clear browsing data
- Firefox: Settings → Privacy → Clear Data
- Safari: Develop → Empty Caches
- Edge: Settings → Privacy → Clear browsing data

### Data Not Updating

**Symptoms:**
- Old prices showing
- Signals delayed
- Charts frozen

**Solutions:**
1. Click refresh button
2. Check market hours
3. Verify data feed (Health page)
4. Re-login
5. Contact support

### Charts Not Loading

**Symptoms:**
- Blank chart area
- Error message
- Spinning loader

**Solutions:**
1. Refresh page
2. Check date range
3. Try different chart type
4. Reduce data points
5. Update browser

## Broker Connection

### Can't Connect Broker

**Symptoms:**
- Connection fails
- Invalid credentials
- API error

**Setup Checklist:**

| Step | Action |
|------|--------|
| **1. Enable API** | In broker account settings |
| **2. Get credentials** | Copy API key exactly |
| **3. Check permissions** | Read/write enabled |
| **4. IP whitelist** | Add Sigmatiq IPs if needed |
| **5. Test connection** | Use test button |

### Orders Not Sending

**Symptoms:**
- Signals not executing
- Orders rejected
- Error messages

**Common Fixes:**
1. Check account balance
2. Verify market hours
3. Check position limits
4. Review order types
5. Test with small order

## Account Issues

### Subscription Problems

**Can't upgrade/downgrade:**
1. Check payment method
2. Wait for current period end
3. Clear browser cache
4. Try different browser
5. Contact billing support

**Not seeing premium features:**
1. Log out and back in
2. Check subscription status
3. Refresh page
4. Clear cache
5. Contact support

### Data Export Issues

**Can't download CSV:**
1. Check browser downloads folder
2. Disable popup blocker
3. Try right-click → Save as
4. Use different browser
5. Check disk space

## Mobile Issues

### Mobile Site Problems

**Common issues:**
- Buttons too small
- Charts not showing
- Can't scroll

**Solutions:**
1. Use landscape mode
2. Zoom out to 90%
3. Try desktop mode
4. Use tablet instead
5. Wait for mobile app

## Error Messages

### Common Errors Explained

| Error | Meaning | Fix |
|-------|---------|-----|
| **"Rate limited"** | Too many requests | Wait 1 minute |
| **"Session expired"** | Logged out | Log in again |
| **"Insufficient permissions"** | No access | Check subscription |
| **"Invalid parameter"** | Wrong input | Check field values |
| **"Server error"** | Our problem | Wait and retry |

## When to Contact Support

Contact support if:
- Problem persists after trying fixes
- See error code (save it)
- Lost access to account
- Billing issues
- Data looks wrong
- Security concerns

**Before contacting:**
1. Note exact error message
2. Screenshot the problem
3. List steps to reproduce
4. Include browser/device info
5. Check if others have same issue

## Quick Fix Checklist

Try these first for any problem:

- [ ] Refresh the page
- [ ] Clear browser cache
- [ ] Log out and back in
- [ ] Try different browser
- [ ] Check system health page
- [ ] Verify market hours
- [ ] Review recent changes
- [ ] Check community forum

## Browser Requirements

**Supported Browsers:**
- Chrome 90+ ✓
- Firefox 88+ ✓
- Safari 14+ ✓
- Edge 90+ ✓

**Not Supported:**
- Internet Explorer ✗
- Old browser versions ✗
- Mobile browsers (limited) ⚠

## System Status

Check current system status:
1. Go to Health page
2. Look for green checks
3. Note any warnings
4. Check planned maintenance

**Status Indicators:**
- **Green**: Working normally
- **Yellow**: Degraded performance
- **Red**: Major issues
- **Gray**: Maintenance mode

## Prevention Tips

Avoid problems by:
1. Using modern browser
2. Stable internet connection
3. Following limits
4. Reading error messages
5. Testing changes small
6. Keeping notes
7. Regular backups/exports

## Still Stuck?

If nothing works:
1. Check [FAQ](./faq.md) for more help
2. Search community forum
3. Contact support chat
4. Email detailed description
5. Book support call (Premium)

---

## Related Reading

- [FAQ](./faq.md)
- [Getting Started](../getting-started.md)
- [System Health](../products/options-health.md)
- [Dashboard](../products/dashboard.md)
- [Models](../products/models.md)