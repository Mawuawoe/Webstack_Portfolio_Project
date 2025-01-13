from models import storage
from models.pan import Pan

# Define initial pan data
pan_data = [
    ("R1", 1000, "Reservoir"),
    ("R2", 1000, "Reservoir"),
    ("R3", 1000, "Reservoir"),
    ("R4", 1000, "Reservoir"),
    ("R5", 1000, "Reservoir"),
    ("PCRA", 500, "PCR"),
    ("PCRB", 500, "PCR")
]

# Add pan1 to pan32 dynamically
for i in range(1, 33):
    pan_data.append((f"Pan{i}", 750, "Pan"))

# Function to seed initial data
def seed_data():
    # Check if any Pan objects exist
    if not storage.all(Pan).values():
        print("Seeding initial data...")
        for pan_id, size, pan_type in pan_data:
            # Create a Pan object
            pan = Pan(
                pan_id=pan_id,
                size=size,
                location="Agbekpe",
                pan_type=pan_type
            )
            storage.new(pan)  # Add to storage
        storage.save()  # Persist changes
        print("Seeding complete!")
    else:
        print("Data already seeded. Skipping seeding process.")

# Call seed_data during app startup
seed_data()
