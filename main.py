from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify your frontend's origin instead
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# Load the dataset
df = pd.read_csv('cleaned_planets.csv')

# Function to search for planets based on input criteria
def search_planet(stars: Optional[int] = None, moons: Optional[int] = None, 
                  disc_year: Optional[int] = None, orbital_period: Optional[float] = None, 
                  radius: Optional[float] = None, mass: Optional[float] = None, 
                   solar_radius: Optional[float] = None, 
                  solar_mass: Optional[float] = None, rotational_velocity: Optional[float] = None, 
                  distance: Optional[float] = None, gaia_magnitude: Optional[float] = None):
    
    # Adjusted tolerances for approximate search
    orbital_period_tol = 110
    radius_tol = 1
    mass_tol = 2000
    solar_radius_tol = 2
    solar_mass_tol = 0.5
    rotational_velocity_tol = 1
    distance_tol = 50
    gaia_magnitude_tol = 1
    
    conditions = []
    
    # Exact match for categorical fields (stars, moons, disc_year)
    if stars is not None and stars >= 0:
        conditions.append(df['stars'] == stars)
    if moons is not None and moons >= 0:
        conditions.append(df['moons'] == moons)
    if disc_year is not None and disc_year >= 1990:
        conditions.append(df['disc_year'] == disc_year)

    # Approximate matches for numerical fields with adjusted tolerances
    if orbital_period is not None and orbital_period >= 0:
        conditions.append((df['orbital period'] >= orbital_period - orbital_period_tol) & 
                          (df['orbital period'] <= orbital_period + orbital_period_tol))
    if radius is not None and radius >= 0:
        conditions.append((df['radius'] >= radius - radius_tol) & 
                          (df['radius'] <= radius + radius_tol))
    if mass is not None and mass >= 0:
        conditions.append((df['mass'] >= mass - mass_tol) & 
                          (df['mass'] <= mass + mass_tol))
    if solar_radius is not None and solar_radius >= 0:
        conditions.append((df['solar radius'] >= solar_radius - solar_radius_tol) & 
                          (df['solar radius'] <= solar_radius + solar_radius_tol))
    if solar_mass is not None and solar_mass >= 0:
        conditions.append((df['solar mass'] >= solar_mass - solar_mass_tol) & 
                          (df['solar mass'] <= solar_mass + solar_mass_tol))
    if rotational_velocity is not None and rotational_velocity >= 0:
        conditions.append((df['rotational velocity'] >= rotational_velocity - rotational_velocity_tol) & 
                          (df['rotational velocity'] <= rotational_velocity + rotational_velocity_tol))
    if distance is not None and distance >= 0:
        conditions.append((df['distance'] >= distance - distance_tol) & 
                          (df['distance'] <= distance + distance_tol))
    if gaia_magnitude is not None and gaia_magnitude >= 0:
        conditions.append((df['gaia magnitude'] >= gaia_magnitude - gaia_magnitude_tol) & 
                          (df['gaia magnitude'] <= gaia_magnitude + gaia_magnitude_tol))

    # Combine all conditions
    if conditions:
        combined_conditions = conditions[0]
        for condition in conditions[1:]:
            combined_conditions &= condition
        filtered_df = df[combined_conditions]
    else:
        filtered_df = df

    # Return the filtered DataFrame or message
    if not filtered_df.empty:
        return filtered_df[['pl_name', 'orbital period', 'radius', 'mass', 'distance']].to_dict(orient='records')
    else:
        return {"message": "No matching planets found"}

# Define the FastAPI route for searching planets
@app.get("/search/")
async def search_planets(
    stars: Optional[int] = Query(None, description="Number of stars"),
    moons: Optional[int] = Query(None, description="Number of moons"),
    disc_year: Optional[int] = Query(None, description="Discovery year"),
    orbital_period: Optional[float] = Query(None, description="Orbital period"),
    radius: Optional[float] = Query(None, description="Planet radius"),
    mass: Optional[float] = Query(None, description="Planet mass"),
    solar_radius: Optional[float] = Query(None, description="Solar radius"),
    solar_mass: Optional[float] = Query(None, description="Solar mass"),
    rotational_velocity: Optional[float] = Query(None, description="Rotational velocity"),
    distance: Optional[float] = Query(None, description="Distance from Earth"),
    gaia_magnitude: Optional[float] = Query(None, description="Gaia magnitude"),
):
    results = search_planet(
        stars=stars,
        moons=moons,
        disc_year=disc_year,
        orbital_period=orbital_period,
        radius=radius,
        mass=mass,
        solar_radius=solar_radius,
        solar_mass=solar_mass,
        rotational_velocity=rotational_velocity,
        distance=distance,
        gaia_magnitude=gaia_magnitude
    )
    return results
