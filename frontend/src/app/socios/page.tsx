"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/api/socios";

export default function SociosPage() {
  const [socios, setSocios] = useState([]);
  const [formData, setFormData] = useState({ dni: "", nombre_completo: "", correo: "" });
  const [cargando, setCargando] = useState(false);

  const cargarSocios = () => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => setSocios(data));
  };

  useEffect(() => {
    cargarSocios();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCargando(true);
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    setFormData({ dni: "", nombre_completo: "", correo: "" });
    cargarSocios();
    setCargando(false);
  };

  const handleBaja = async (id) => {
    if (confirm("¿Estás seguro de dar de baja a este socio? (Sus datos históricos se conservarán)")) {
      await fetch(`${API_URL}/${id}/baja`, { method: "PUT" });
      cargarSocios();
    }
  };

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Socios</h2>
          <p className="text-muted-foreground">Gestiona los miembros de la asociación.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-4 gap-4 rounded-lg border p-4 bg-card shadow-sm">
        <div className="space-y-2">
          <Label htmlFor="dni">DNI</Label>
          <Input id="dni" placeholder="Ej: 12345678" value={formData.dni} onChange={(e) => setFormData({...formData, dni: e.target.value})} required />
        </div>
        <div className="space-y-2">
          <Label htmlFor="nombre">Nombre Completo</Label>
          <Input id="nombre" placeholder="Juan Perez" value={formData.nombre_completo} onChange={(e) => setFormData({...formData, nombre_completo: e.target.value})} required />
        </div>
        <div className="space-y-2">
          <Label htmlFor="correo">Correo</Label>
          <Input id="correo" type="email" placeholder="juan@email.com" value={formData.correo} onChange={(e) => setFormData({...formData, correo: e.target.value})} required />
        </div>
        <div className="flex items-end">
          <Button type="submit" className="w-full" disabled={cargando}>
            {cargando ? "Guardando..." : "+ Alta de Socio"}
          </Button>
        </div>
      </form>

      <div className="rounded-md border bg-card shadow-sm">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">DNI</TableHead>
              <TableHead>Nombre Completo</TableHead>
              <TableHead>Correo</TableHead>
              <TableHead className="text-right">Estado</TableHead>
              <TableHead className="text-right">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {socios.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                  No hay socios cargados.
                </TableCell>
              </TableRow>
            ) : (
              socios.map((socio) => (
                <TableRow key={socio.id} className={!socio.activo ? "opacity-50" : ""}>
                  <TableCell className="font-medium">{socio.dni}</TableCell>
                  <TableCell>{socio.nombre}</TableCell>
                  <TableCell>{socio.correo}</TableCell>
                  <TableCell className="text-right font-semibold">
                    {socio.activo ? (
                      <span className="text-green-600">Activo</span>
                    ) : (
                      <span className="text-red-600">De Baja</span>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    {socio.activo && (
                      <Button variant="destructive" size="sm" onClick={() => handleBaja(socio.id)}>
                        Dar de Baja
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

