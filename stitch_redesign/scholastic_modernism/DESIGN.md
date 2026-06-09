---
name: Scholastic Modernism
colors:
  surface: '#faf8ff'
  surface-dim: '#d9d9e1'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3fb'
  surface-container: '#ededf5'
  surface-container-high: '#e8e7f0'
  surface-container-highest: '#e2e2ea'
  on-surface: '#1a1b21'
  on-surface-variant: '#434652'
  inverse-surface: '#2e3036'
  inverse-on-surface: '#f0f0f8'
  outline: '#737783'
  outline-variant: '#c3c6d4'
  surface-tint: '#2b5bb5'
  primary: '#003178'
  on-primary: '#ffffff'
  primary-container: '#0d47a1'
  on-primary-container: '#a1bbff'
  inverse-primary: '#b0c6ff'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#8df5e4'
  on-secondary-container: '#007165'
  tertiary: '#1e3843'
  on-tertiary: '#ffffff'
  tertiary-container: '#354f5b'
  on-tertiary-container: '#a5c0ce'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d9e2ff'
  primary-fixed-dim: '#b0c6ff'
  on-primary-fixed: '#001945'
  on-primary-fixed-variant: '#00429c'
  secondary-fixed: '#8df5e4'
  secondary-fixed-dim: '#70d8c8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#cbe7f5'
  tertiary-fixed-dim: '#afcbd8'
  on-tertiary-fixed: '#021f29'
  on-tertiary-fixed-variant: '#304a55'
  background: '#faf8ff'
  on-background: '#1a1b21'
  surface-variant: '#e2e2ea'
  status-present: '#2E7D32'
  status-absent: '#D32F2F'
  status-late: '#F57C00'
  surface-subtle: '#F8FAFC'
  border-low-contrast: '#E2E8F0'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  container-max: 1440px
---

## Brand & Style

This design system is built on the principles of **Corporate Modernism** with a specific focus on educational accessibility. It prioritizes clarity, structural integrity, and emotional stability to support the high-stakes environment of school administration. 

The visual language balances the authority of a financial institution with the approachability of a modern learning platform. It avoids "AI-generic" aesthetics by utilizing intentional whitespace, purposeful color coding for data visualization, and a "document-first" philosophy that treats attendance records with the same importance as institutional reports. The emotional goal is to provide teachers and administrators with a sense of calm control and absolute clarity.

## Colors

The palette is anchored by "Academic Blue" and "Trustworthy Teal," colors chosen for their historical association with institutional reliability. 

- **Primary (Blue):** Used for core navigation, primary actions, and branding. It provides a stable foundation for the interface.
- **Secondary (Teal):** Used for instructional elements, success states, and secondary data visualizations.
- **Functional Colors:** These are strictly reserved for status. **Status-Present (Green)** and **Status-Absent (Red)** must never be used for decorative purposes to ensure instant cognitive recognition during attendance taking.
- **Neutral Scale:** A range of cool-toned grays (`#F8FAFC` to `#1E293B`) is used to manage visual hierarchy and separate data-heavy tables from the global navigation.

## Typography

The typography system relies on **Inter** to provide maximum legibility across high-density data tables and small-screen mobile devices. 

- **Hierarchy:** Use `headline-lg` for dashboard titles and `title-lg` for section headers within cards.
- **Data Density:** `body-md` is the workhorse for student lists and attendance grids.
- **Captions:** Use `label-md` in uppercase with letter-spacing for non-interactive metadata or table headers to distinguish them from actionable text.
- **Line Heights:** Generous line heights (1.5x for body text) are maintained to reduce cognitive load during long periods of data entry.

## Layout & Spacing

The design system uses a **Fixed Grid** approach for desktop dashboards to ensure data remains predictable and readable. 

- **Grid System:** A 12-column grid with 24px gutters. Content is centered in a container with a maximum width of 1440px.
- **Rhythm:** All margins and paddings must be multiples of 4px. Use 16px (4 units) for internal component padding and 24px (6 units) for spacing between layout blocks.
- **Mobile Adaptivity:** On mobile, margins shrink to 16px. Vertical stacks are preferred for attendance lists, with "Sticky" headers for student names to maintain context while scrolling through dates.
- **Whitespace:** Emphasize "Breathable Data." Never allow table cells to touch; maintain a minimum of 12px vertical padding within rows.

## Elevation & Depth

This design system uses **Tonal Layers** supplemented by **Ambient Shadows** to create a structured hierarchy without visual clutter.

- **Surface Levels:** The primary background is `white`. Secondary containers (like sidebars or table headers) use `surface-subtle`.
- **Shadows:** Use extremely soft, low-opacity shadows for interactive cards. (Example: `0px 4px 12px rgba(13, 71, 161, 0.05)`). This "tinted shadow" creates a subtle connection to the brand primary color.
- **Borders:** Use `border-low-contrast` (1px) for all static containers. Use the Primary color for borders on focused input fields to signal activity.
- **Interactive Depth:** On hover, cards should lift slightly (increasing shadow spread) rather than changing background color, preserving the readability of the internal text.

## Shapes

The shape language is consistently **Rounded** (8px to 12px) to soften the institutional nature of an attendance system and make the software feel supportive.

- **Buttons & Inputs:** Use the base 8px (`rounded-md`) radius.
- **Cards & Modals:** Use 16px (`rounded-lg`) to create a clear container distinction.
- **Status Chips:** Use 4px (`rounded-sm`) for status indicators within tables to maintain a "tag" aesthetic that doesn't compete with larger UI elements.
- **Avatars:** Always circular to provide a organic counterpoint to the rigid grid of attendance data.

## Components

- **Attendance Buttons:** Use large, tactile toggle buttons for "Present" and "Absent." When active, they should use high-contrast fills (Green/Red); when inactive, they should use a subtle outline.
- **Data Tables:** Headers should be sticky. Rows must have a subtle hover state (`surface-subtle`) to help the eye track across long horizontal lines of data.
- **Cards:** Dashboard summaries (e.g., "Total Absence Rate") should be housed in 16px rounded cards with a subtle blue-tinted shadow.
- **Input Fields:** Use floating labels to save vertical space. Validation states (error/success) must use functional colors and accompanying icons for accessibility.
- **Progress Bars:** Use for "Term Completion" or "Class Attendance Average," utilizing the Secondary Teal color to indicate positive growth.
- **Filter Chips:** Small, 4px rounded tags used above tables to allow teachers to quickly filter by "Excused," "Unexcused," or "Late" statuses.