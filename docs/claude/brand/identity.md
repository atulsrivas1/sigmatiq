# Sigmatiq Brand Identity

## Visual Design and Voice Guidelines

This page describes the Sigmatiq brand: our colors, icons, and how we communicate.

## Brand Colors

### Primary Palette

Our main colors create a professional, trustworthy feel:

| Color Name | Hex Code | Where It's Used |
|------------|----------|-----------------|
| **Dark Teal** | `#1A2F2F` | Main backgrounds, headers |
| **Bright Teal** | `#00C4A7` | Primary buttons, active states |
| **Deep Teal** | `#00D4B8` | Hover effects, accents |
| **Light Teal** | `#00E5CC` | Highlights, badges |
| **Golden** | `#FFB800` | Warnings, important items |
| **Cream** | `#E8E3D9` | Light backgrounds (Slate theme) |
| **Gray** | `#F5F5F7` | Text, interface elements |

### Pack-Specific Colors

Each trading pack has its own accent color:

| Pack Name | Color | Hex Code | Meaning |
|-----------|-------|----------|---------|
| **ZeroSigma** | Blue | `#3B82F6` | Fast, precise |
| **SwingSigma** | Orange | `#F97316` | Active, energetic |
| **LongSigma** | Green | `#22C55E` | Growth, patience |
| **OvernightSigma** | Purple | `#8B5CF6` | Mystery, opportunity |
| **MomentumSigma** | Pink | `#EC4899` | Dynamic, flowing |
| **CustomSigma** | Teal | `#14B8A6` | Flexible, personal |

### Status Colors

We use consistent colors for status indicators:

| Status | Color | Hex Code | Used For |
|--------|-------|----------|----------|
| **Success** | Green | `#10B981` | Pass, complete, good |
| **Warning** | Yellow | `#F59E0B` | Caution, review needed |
| **Error** | Red | `#EF4444` | Fail, stop, problem |
| **Info** | Blue | `#3B82F6` | Information, in progress |
| **Neutral** | Gray | `#6B7280` | Inactive, disabled |

## Theme System

Sigmatiq offers four visual themes:

### 1. Dark Theme (Default)
- **Background**: Dark teal (`#1A2F2F`)
- **Text**: Light gray (`#F5F5F7`)
- **Feel**: Professional, focused

### 2. Light Theme
- **Background**: White (`#FFFFFF`)
- **Text**: Dark gray (`#1F2937`)
- **Feel**: Clean, bright

### 3. Slate Theme  
- **Background**: Cream (`#E8E3D9`)
- **Text**: Dark brown (`#3E2723`)
- **Feel**: Warm, comfortable

### 4. Midnight Theme
- **Background**: Near black (`#0A0E0E`)
- **Text**: Light gray (`#E5E7EB`)
- **Feel**: Minimal, intense

## Typography

### Font Families

**Primary Font Stack:**
```
Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
```

**Monospace Font Stack:**
```
Monaco, Menlo, Consolas, 'Courier New', monospace
```

### Font Usage

| Element | Font | Size | Weight |
|---------|------|------|--------|
| **Page Title** | Inter | 32px | Bold |
| **Section Header** | Inter | 24px | Semibold |
| **Body Text** | Inter | 14px | Regular |
| **Small Text** | Inter | 12px | Regular |
| **Model IDs** | Monaco | 13px | Regular |
| **Code/Data** | Monaco | 12px | Regular |

## Icon Set

### Navigation Icons
- **Dashboard**: Grid of squares (`⊞`)
- **Models**: Cube (`◧`)
- **Signals**: Radio waves (`〰`)
- **Sweeps**: Grid dots (`⋮⋮⋮`)
- **Leaderboard**: Trophy (`🏆`)
- **Health**: Heart (`♥`)
- **Settings**: Gear (`⚙`)

### Action Icons
- **Create**: Plus circle (`⊕`)
- **Edit**: Pencil (`✏`)
- **Delete**: Trash can (`🗑`)
- **Run**: Play button (`▶`)
- **Stop**: Square (`■`)
- **Refresh**: Circular arrows (`↻`)
- **Download**: Down arrow (`↓`)
- **Upload**: Up arrow (`↑`)

### Status Icons
- **Success**: Check mark (`✓`)
- **Error**: X mark (`✗`)
- **Warning**: Triangle (`⚠`)
- **Info**: Circle i (`ⓘ`)
- **Loading**: Spinner (`◐`)

### Trading Icons
- **Buy/Long**: Up arrow (`↑`)
- **Sell/Short**: Down arrow (`↓`)
- **Hold**: Horizontal line (`—`)
- **Stop Loss**: Shield (`🛡`)

## Tone of Voice

### Our Personality
- **Clear**: We explain complex things simply
- **Confident**: We know our system works
- **Helpful**: We want you to succeed
- **Honest**: We tell you the risks

### Writing Style

**We say:**
- "Create your first model" (simple, direct)
- "This strategy lost money" (honest)
- "Start with paper trading" (helpful)

**We don't say:**
- "Leverage our proprietary algorithms" (jargon)
- "Guaranteed profits" (misleading)
- "Simply click here" (condescending)

### Key Messages

**Primary Tagline:**
"Intelligence You Can Trust"

**Supporting Messages:**
- "Professional trading tools for everyone"
- "Test before you trade"
- "Your strategies, automated safely"

## Visual Patterns

### Card Design
- Rounded corners (8px radius)
- Subtle shadow on hover
- Border in theme accent color
- Padding: 16px minimum

### Button Styles

**Primary Button:**
- Background: Bright Teal (`#00C4A7`)
- Text: White
- Hover: Deep Teal (`#00D4B8`)
- Padding: 8px 16px
- Radius: 6px

**Secondary Button:**
- Background: Transparent
- Border: 1px solid current color
- Hover: Light background
- Same padding and radius

### Table Design
- Alternating row colors (subtle)
- Hover highlight on rows
- Sortable column headers with arrows
- Right-align numbers
- Left-align text

### Badge Design
- Rounded pill shape
- Small text (11px)
- Colored background
- White or dark text for contrast

## Component Examples

### Gate Badge
- **Pass**: Green background, check icon
- **Fail**: Red background, X icon
- Shows reason on hover

### Confidence Badge
- Number percentage
- Color gradient (red → yellow → green)
- Higher number = greener color

### Pack Badge
- Pack color background
- White text
- Pack name abbreviated

## Spacing System

We use consistent spacing:

| Name | Size | Use Case |
|------|------|----------|
| **xs** | 4px | Between related items |
| **sm** | 8px | Inside components |
| **md** | 16px | Between components |
| **lg** | 24px | Between sections |
| **xl** | 32px | Page margins |

## Responsive Design

### Breakpoints
- **Mobile**: < 640px (not primary focus)
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px (optimized for this)

### Priority
Desktop-first design since trading requires multiple data views.

## Animation

### Transitions
- Duration: 200ms for most
- Easing: ease-in-out
- Properties: opacity, transform

### Loading States
- Skeleton screens for tables
- Spinning icon for actions
- Progress bars for long operations

## Accessibility

### Color Contrast
- Minimum 4.5:1 for normal text
- Minimum 3:1 for large text
- Test all color combinations

### Focus States
- Visible outline on all interactive elements
- Keyboard navigation supported
- Skip links provided

## Brand Application

### Do's ✓
- Use official colors
- Keep spacing consistent
- Write clearly and simply
- Show real data

### Don'ts ✗
- Create new colors
- Use multiple fonts
- Write complex jargon
- Make false promises

---

## Related Reading

- [Getting Started](../getting-started.md)
- [Dashboard](../products/dashboard.md)
- [Suite Overview](../suite/overview.md)
- [Models](../products/models.md)
- [FAQ](../help/faq.md)