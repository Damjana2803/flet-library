# Database Seeder Documentation

## Overview

The Library Management System includes a comprehensive database seeder that automatically populates the database with sample data for development and testing purposes.

## Features

### 🔐 Admin User
- **Email**: `admin@biblioteka.rs`
- **Password**: `admin123`
- **Type**: Administrator with full access

### 👥 Sample Members (6 users)
Each member has a user account with login credentials:

| Name | Email | Password | Membership Type | Max Loans |
|------|-------|----------|----------------|-----------|
| Damjana Zubac | `dada@gmail.com` | `dada123` | Regular | 5 |
| Djordje Zubac | `djordje.zubac@w3-lab.com` | `djordje.zubac123` | Student | 3 |
| Ana Petrović | `ana.petrovic@gmail.com` | `ana.petrovic123` | Regular | 5 |
| Marko Jovanović | `marko.jovanovic@yahoo.com` | `marko.jovanovic123` | Senior | 7 |
| Jelena Nikolić | `jelena.nikolic@hotmail.com` | `jelena.nikolic123` | Student | 3 |
| Stefan Đorđević | `stefan.djordjevic@gmail.com` | `stefan.djordjevic123` | Regular | 5 |

### 📚 Sample Books (13 books)
Books with various quantities to test different scenarios:

#### Out of Stock (0 copies)
- **1984** by Đordž Orvel
- **Veliki Getsbi** by F. Skot Ficdžerald

#### Limited Stock (1 copy each)
- **Ubijati pticu rugalicu** by Harper Li
- **Gordost i predrasude** by Džejn Ostin
- **Lovac u žitu** by Dž. D. Selindžer
- **Umetnost rata** by Sun Cu

#### Multiple Copies (2-4 copies)
- **Hobit** by Dž. R. R. Tolkin (3 copies)
- **Gospodar prstenova** by Dž. R. R. Tolkin (2 copies)
- **Hari Poter i kamen mudraca** by Dž. K. Rouling (4 copies)
- **Alhemičar** by Paulo Koeljo (2 copies)
- **Mali princ** by Antoan de Sent Egziperi (3 copies)
- **Sapiens: Kratka istorija čovečanstva** by Juval Noa Harari (2 copies)
- **Psihologija novca** by Morgan Hausel (2 copies)

### 🔗 Sample Data
- **2 Active Loans**: Damjana borrowed "Ubijati pticu rugalicu", Djordje borrowed "Gordost i predrasude"
- **2 Active Reservations**: Ana reserved "1984", Marko reserved "Veliki Getsbi"

## How It Works

### Automatic Seeding
The seeder runs automatically when:
1. Database is first initialized (`db_init()`)
2. Database is empty or seeder hasn't run before

### Seeding State Tracking
- Creates a `seeder_state` table to track if seeding has been completed
- Prevents duplicate seeding on subsequent runs
- Can be manually reset if needed

### Safety Features
- **Duplicate Prevention**: Checks if data already exists before creating
- **Error Handling**: Graceful error handling with detailed logging
- **Transaction Safety**: Uses database transactions for data integrity

## Usage

### Automatic (Recommended)
The seeder runs automatically when you start the application for the first time:

```bash
python src/main.py
```

### Manual Seeding
If you need to run the seeder manually:

```bash
python src/utils/seeder.py
```

### Reset Seeding State
To force re-seeding (useful for testing):

```sql
UPDATE seeder_state SET seeded = FALSE WHERE id = 1;
```

## Database Schema

### Seeder State Table
```sql
CREATE TABLE seeder_state (
    id INTEGER PRIMARY KEY,
    seeded BOOLEAN DEFAULT FALSE,
    seeded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Sample Data Structure
The seeder creates realistic data with:
- **Proper relationships** between users, members, books, loans, and reservations
- **Realistic dates** (current dates for loans, future dates for due dates)
- **Proper quantities** (available_copies updated when books are loaned)
- **Member loan counts** (current_loans updated when books are borrowed)

## Testing Scenarios

The seeded data allows testing of various scenarios:

### 📖 Book Management
- **Out of stock books**: Cannot be borrowed or reserved
- **Limited stock**: Only one copy available
- **Multiple copies**: Several copies available
- **Different categories**: Fiction, Fantasy, History, Military, Psychology

### 👥 Member Management
- **Different membership types**: Student (3 loans), Regular (5 loans), Senior (7 loans)
- **Active loans**: Members with borrowed books
- **Active reservations**: Members with reserved books

### 🔐 Authentication
- **Admin login**: Full administrative access
- **Member login**: Limited member access
- **Password validation**: Real password hashing

### 📊 Statistics
- **Dashboard statistics**: Real data for admin dashboard
- **Member statistics**: Current loans, available capacity
- **Book statistics**: Total copies, available copies

## Troubleshooting

### Seeder Not Running
If the seeder doesn't run automatically:
1. Check if `seeder_state` table exists
2. Verify database permissions
3. Check console output for error messages

### Duplicate Data
If you see duplicate data:
1. The seeder includes duplicate prevention
2. Check if data was manually added
3. Verify seeder state tracking

### Reset Database
To completely reset the database:
1. Delete `database.db` file
2. Restart the application
3. Seeder will run automatically on fresh database

## Development Notes

### Adding New Sample Data
To add more sample data:
1. Edit the data arrays in `src/utils/seeder.py`
2. Follow the existing data structure
3. Test with a fresh database

### Customizing Seeder
The seeder is modular and can be easily customized:
- Add new member types
- Include more book categories
- Modify loan/reservation patterns
- Add more realistic data

### Performance
The seeder is optimized for:
- **Fast execution**: Minimal database operations
- **Memory efficiency**: Processes data in batches
- **Error recovery**: Continues on individual item failures

## Security Notes

### Default Passwords
⚠️ **Important**: The seeded accounts use simple passwords for development/testing only.

**For production use:**
- Change all default passwords
- Use strong password policies
- Implement password reset functionality
- Consider removing seeded data

### Data Privacy
The sample data uses fictional names and addresses. For production:
- Use anonymized data
- Remove personal information
- Follow data protection regulations

## Support

If you encounter issues with the seeder:
1. Check the console output for error messages
2. Verify database file permissions
3. Ensure all required tables exist
4. Check the seeder state tracking

The seeder is designed to be robust and provide clear feedback about its operation.
