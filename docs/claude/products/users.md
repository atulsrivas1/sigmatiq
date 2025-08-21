# Users

## Managing Users and Access

The Users section lets administrators manage who can access Sigmatiq and what they can do.

## What It Is

Users management controls:
- Who can log in
- What features they access
- Trading permissions
- Account limits
- Team organization

Think of it as the membership desk - controlling who gets in and what they can do.

## Why It Matters

User management helps:
- Keep platform secure
- Control costs
- Organize teams
- Track usage
- Ensure compliance

## Key Concepts

### User Roles

| Role | Access Level | Can Do |
|------|--------------|--------|
| **Viewer** | Read-only | Look but not trade |
| **Trader** | Standard | Create and trade strategies |
| **Premium** | Enhanced | Everything plus automation |
| **Manager** | Team lead | Manage team members |
| **Admin** | Full control | Everything including settings |

### User Status

| Status | Meaning | Can Login? |
|--------|---------|------------|
| **Active** | Normal user | Yes |
| **Suspended** | Temporarily blocked | No |
| **Inactive** | Not used recently | Yes |
| **Locked** | Too many bad logins | No |
| **Deleted** | Removed from system | No |

### Permissions

What users can do:
- View data
- Create models
- Run backtests
- Trade live
- Use automation
- Access admin

## Main Screen Tour

*Note: Admin or Manager access required*

### Users List

Main table showing:

#### User Information
- **Name**: Full name
- **Email**: Login email
- **Username**: Display name
- **User ID**: System identifier
- **Created**: Join date
- **Last Active**: Recent login

#### Account Details
- **Role**: Permission level
- **Status**: Active/Inactive/etc
- **Plan**: Subscription type
- **Usage**: Resource consumption
- **Models**: Count of strategies

#### Actions
- **Edit**: Change settings
- **Reset Password**: Force reset
- **Suspend**: Temporary block
- **Delete**: Remove user
- **Login As**: Impersonate (admin only)

### User Detail View

Click any user to see:

#### Profile Section
- Personal information
- Contact details
- Profile picture
- Timezone setting
- Language preference

#### Permissions Tab
- Role assignment
- Feature access
- Trading limits
- API permissions
- Special flags

#### Activity Tab
- Login history
- Recent actions
- Models created
- Trades executed
- Support tickets

#### Usage Tab
- Resource consumption
- API calls
- Storage used
- Compute time
- Cost allocation

## Typical Workflows

### Adding New User

1. **Click Add User**
   - Enter email
   - Set temporary password
   - Choose role
   - Set limits

2. **Configure Access**
   - Select features
   - Set quotas
   - Assign to team
   - Enable trading

3. **Send Invitation**
   - Email sent automatically
   - Includes login instructions
   - Temporary password
   - Getting started guide

### Managing Team Members

1. **View Team**
   - Filter by team
   - See all members
   - Check activity

2. **Adjust Permissions**
   - Promote/demote roles
   - Change access levels
   - Set team limits

3. **Monitor Usage**
   - Track consumption
   - Identify heavy users
   - Optimize allocation

### Handling Issues

#### Locked Account
1. Verify identity
2. Check security
3. Reset password
4. Unlock account

#### Suspicious Activity
1. Review logs
2. Contact user
3. Suspend if needed
4. Investigate fully

#### Over Quota
1. Check usage
2. Notify user
3. Upgrade plan
4. Or reduce limits

## User Roles Explained

### Viewer Role
**Can:**
- View public strategies
- See performance data
- Read documentation
- Use paper trading

**Cannot:**
- Create models
- Trade real money
- Change settings
- Access admin

**For:** Learning, monitoring only

### Trader Role
**Can:**
- Everything Viewer can do
- Create models
- Run backtests
- Trade with limits
- Save strategies

**Cannot:**
- Use automation
- Unlimited models
- Admin functions
- Manage others

**For:** Most users

### Premium Role
**Can:**
- Everything Trader can do
- Automated trading
- Unlimited models
- Priority support
- Advanced features

**Cannot:**
- Admin functions
- Manage users
- Change system settings

**For:** Power users

### Manager Role
**Can:**
- Everything Premium can do
- Manage team members
- View team usage
- Allocate resources
- Run reports

**Cannot:**
- System administration
- Global settings
- Delete users
- Access billing

**For:** Team leaders

### Admin Role
**Can:**
- Everything
- System settings
- User management
- Billing access
- Feature flags
- Emergency controls

**For:** System administrators

## Permissions Management

### Setting Permissions

Granular controls:

#### Trading Permissions
- [ ] Paper trading
- [ ] Live trading
- [ ] Options trading
- [ ] Automated execution
- [ ] High-frequency trading

#### Model Permissions
- [ ] Create models
- [ ] Edit models
- [ ] Delete models
- [ ] Share models
- [ ] Clone others' models

#### Data Permissions
- [ ] View real-time data
- [ ] Download data
- [ ] API access
- [ ] Historical data
- [ ] Export reports

### Limits and Quotas

Set boundaries:

| Limit Type | Default | Maximum |
|------------|---------|---------|
| **Models** | 10 | 100 |
| **Backtests/day** | 50 | 500 |
| **API calls/hour** | 1000 | 10000 |
| **Storage** | 1GB | 10GB |
| **Positions** | 10 | 50 |

### Team Management

Organize users:

**Creating Teams:**
1. Name team
2. Set team limits
3. Assign manager
4. Add members

**Team Features:**
- Shared strategies
- Combined quotas
- Team leaderboard
- Collaborative workspace

## User Onboarding

### New User Setup

Automatic process:
1. User receives invitation
2. Creates password
3. Completes profile
4. Gets tutorial
5. Starts with templates

### Training Resources

Provided to new users:
- Welcome email series
- Video tutorials
- Documentation links
- Practice account
- Support contact

### Progress Tracking

Monitor new users:
- Tutorial completion
- First model created
- First backtest run
- First trade executed
- Support tickets

## Security Features

### Authentication

Security measures:
- Strong passwords required
- Two-factor authentication
- Session timeouts
- IP restrictions
- Login notifications

### Audit Trail

Track all actions:
- Login attempts
- Permission changes
- Data access
- Trade execution
- Setting modifications

### Suspicious Activity

Automatic detection:
- Multiple failed logins
- Unusual trading patterns
- Data scraping
- API abuse
- Location changes

## Bulk Operations

### Import Users

Add multiple users:
1. Prepare CSV file
2. Upload to system
3. Validate data
4. Process import
5. Send invitations

### Export Users

Download user data:
- User list CSV
- Activity reports
- Usage statistics
- Audit logs

### Bulk Updates

Change multiple users:
- Role changes
- Status updates
- Limit adjustments
- Team assignments

## Common Issues

### "Can't log in"
- Check status
- Verify email
- Reset password
- Check locks
- Review logs

### "Missing features"
- Check role
- Verify permissions
- Check feature flags
- Review plan

### "Over quota"
- Check usage
- Increase limits
- Upgrade plan
- Contact admin

## Best Practices

### Do's ✓
- Regular audits
- Document changes
- Monitor usage
- Enforce policies
- Train new users

### Don'ts ✗
- Share accounts
- Ignore suspicious activity
- Over-permission
- Skip onboarding
- Delete without backup

## Compliance

### Data Privacy
- GDPR compliance
- Data retention policies
- Right to deletion
- Export capabilities

### Financial Regulations
- Know Your Customer (KYC)
- Anti-money laundering
- Trading restrictions
- Audit requirements

## Reporting

### User Reports

Available reports:
- Active users
- Usage by role
- Login frequency
- Resource consumption
- Cost allocation

### Scheduling

Automatic reports:
- Daily activity
- Weekly summary
- Monthly usage
- Quarterly review

## Next Steps

For administrators:
1. Review user list
2. Audit permissions
3. Check inactive users
4. Optimize quotas
5. Plan onboarding

For managers:
1. Monitor team usage
2. Help struggling users
3. Identify top performers
4. Request resources

## Assumptions & Open Questions

**Assumptions:**
- Email is unique identifier
- Roles are hierarchical
- Teams are separate

**Open Questions:**
- Social login integration
- Guest accounts
- API-only users
- Multi-account support

---

## Related Reading

- [Feature Flags](./feature-flags.md)
- [Admin Jobs](./admin-jobs.md)
- [Risk Profiles](./risk-profiles.md)
- [Getting Started](../getting-started.md)
- [FAQ](../help/faq.md)