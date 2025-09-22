import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

type Props = {
	geojson?: GeoJSON.FeatureCollection;
};

export default function CustomerMap({ geojson }: Props) {
	return (
		<div className="h-[360px] w-full overflow-hidden rounded border border-gray-200 dark:border-gray-800">
			<MapContainer center={[16.047079, 108.20623]} zoom={5} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
				<TileLayer
					attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
					url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
				/>
				{geojson && <GeoJSON data={geojson as any} />}
			</MapContainer>
		</div>
	);
}


